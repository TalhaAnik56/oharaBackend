from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from rest_framework import serializers

from community.models import Customer
from warehouse.models import BookItem
from warehouse.signals import stock_out

from .models import Cart, CartItem, MoneyWithdraw, Order, OrderItem, SellerWallet
from .signals import order_delivered


class SimpleBookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ["id", "book", "seller", "unit_price"]

    book = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "book_item", "unit_price", "quantity", "total_price"]

    book_item = SimpleBookItemSerializer()
    total_price = serializers.SerializerMethodField(method_name="calculated_price")

    def calculated_price(self, cart_item):
        return cart_item.book_item.unit_price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "created_at",
            "cartitem_set",
            "subtotal",
        ]

    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField(
        method_name="calculated_price", read_only=True
    )

    def calculated_price(self, cart: Cart):
        prices = [
            item.book_item.unit_price * item.quantity
            for item in cart.cartitem_set.all()
        ]
        subtotal = sum(prices)
        return subtotal


def is_quantity_greater_than_stock(book_item, quantity):
    if quantity > book_item.stock:
        raise serializers.ValidationError(
            {
                "error": f"Sorry, we only have {book_item.stock} pieces of this book in our stock"
            }
        )


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["book_item", "quantity"]

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        book_item = self.validated_data["book_item"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, book_item__id=book_item.id
            )
            new_quantity = cart_item.quantity + quantity
            is_quantity_greater_than_stock(cart_item.book_item, new_quantity)
            cart_item.quantity = new_quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            is_quantity_greater_than_stock(book_item, quantity)
            cart_item = CartItem.objects.create(
                **self.validated_data, cart_id=cart_id, unit_price=book_item.unit_price
            )
            self.instance = cart_item

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    def save(self, **kwargs):
        quantity = self.validated_data["quantity"]
        cart_item = self.instance
        is_quantity_greater_than_stock(cart_item.book_item, quantity)
        cart_item.quantity = quantity
        cart_item.save()
        self.instance = cart_item
        return self.instance


class Book_Item_Serializer_For_Order_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = [
            "id",
            "book",
            "seller",
        ]

    book = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "book_item", "quantity", "unit_price"]

    book_item = Book_Item_Serializer_For_Order_Item_Serializer()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "payment_status",
            "order_status",
            "delivery_fee",
            "coupon_discount",
            "delivery_address",
            "orderitem_set",
            "total_price",
            "money_transferred",
            "created_at",
        ]

    orderitem_set = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="calculated_price")

    def calculated_price(self, order: Order):
        prices = [item.quantity * item.unit_price for item in order.orderitem_set.all()]
        total_price = sum(prices) + order.delivery_fee - order.coupon_discount
        return total_price


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    delivery_address = serializers.CharField(max_length=200)
    delivery_fee = serializers.IntegerField(
        validators=[
            MinValueValidator(0, "Delivery fee can not be less than zero"),
            MaxValueValidator(300, "Delivery fee can not be greater than 300"),
        ]
    )
    coupon_discount = serializers.IntegerField(
        validators=[
            MinValueValidator(0, "Discount can not be less than zero"),
            MaxValueValidator(3000, "Discount can not be greater than 3000"),
        ]
    )

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart doesn't exist")
        elif CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("There are no products in this cart")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            cart_id = self.validated_data["cart_id"]
            delivery_address = self.validated_data["delivery_address"]
            delivery_fee = self.validated_data["delivery_fee"]
            coupon_discount = self.validated_data["coupon_discount"]

            customer = Customer.objects.get(user_id=user_id)
            cart = Cart.objects.get(pk=cart_id)
            order = Order.objects.create(
                customer=customer,
                delivery_address=delivery_address,
                delivery_fee=delivery_fee,
                coupon_discount=coupon_discount,
            )
            cart_items = CartItem.objects.filter(cart_id=cart.id).select_related(
                "book_item"
            )

            items_total_price = sum(
                [item.unit_price * item.quantity for item in cart_items]
            )
            # Let's check if coupon discount is greater than the books' total price?
            if coupon_discount > items_total_price:
                raise serializers.ValidationError(
                    {
                        "error": "Coupon discount cannot be greater than the books' total price"
                    }
                )

            # Let's create order item objects
            order_items = []
            for item in cart_items:
                quantity = item.quantity
                stock = item.book_item.stock
                if quantity > stock:
                    raise serializers.ValidationError(
                        {
                            "error": f"Sorry, We only have {stock} pieces of this book in our stock"
                        }
                    )

                order_item = OrderItem(
                    order=order,
                    book_item=item.book_item,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                item.book_item.stock -= quantity
                item.book_item.save()
                # If stock becomes zero we will fire a signal
                if item.book_item.stock == 0:
                    stock_out.send_robust(BookItem, book_item=item.book_item)
                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)
            cart.delete()
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status", "order_status"]

    def save(self, **kwargs):
        with transaction.atomic():
            order = self.instance
            payment_status = self.validated_data["payment_status"]
            order_status = self.validated_data["order_status"]

            # Read the error messages, you will understand the logics automatically
            if order.order_status == "D" and order_status != "D":
                raise serializers.ValidationError(
                    {"error": "You can't change the order status once it's delivered"}
                )

            elif order.payment_status == "R" and payment_status != "R":
                raise serializers.ValidationError(
                    {"error": "You can't change the payment status once it's received"}
                )

            elif payment_status != "R" and order_status == "D":
                raise serializers.ValidationError(
                    {"error": "You have to make the payment first"}
                )

            # We will transfer money to sellers' accounts once the order is delivered.
            # For that reason, order delivered shouldn't be updated more than once. So if the user provide "R" as payment_status and "D"
            # as order_status, if the order is already in that state,it won't be updated again.So the money will transfer to the sellers'
            # accounts only once.
            elif (
                order.order_status == "D"
                and order_status == "D"
                and order.payment_status == "R"
                and payment_status == "R"
            ):
                raise serializers.ValidationError(
                    {"error": "The changes you are trying to apply is already applied"}
                )

            order.payment_status = payment_status
            order.order_status = order_status
            order.save()
            self.instance = order
            if order.order_status == "D":
                order_delivered.send_robust(Order, order=order)
            return self.instance


class SellerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerWallet
        fields = ["id", "seller", "total_earned", "balance", "withdrawn", "last_update"]


class MoneyWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyWithdraw
        fields = ["id", "amount", "payment_method", "payment_account_no", "seller"]

    seller = serializers.StringRelatedField(read_only=True)

    def save(self, **kwargs):
        with transaction.atomic():
            seller_id = self.context["seller_id"]
            seller_wallet = SellerWallet.objects.get(seller_id=seller_id)

            amount = self.validated_data["amount"]
            payment_method = self.validated_data["payment_method"]
            payment_account_no = self.validated_data["payment_account_no"]

            if amount > seller_wallet.balance:
                raise serializers.ValidationError(
                    {"error": "You have insufficient balance"}
                )

            money_withdraw = MoneyWithdraw.objects.create(
                seller=seller_wallet.seller,
                amount=amount,
                payment_account_no=payment_account_no,
                payment_method=payment_method,
            )

            seller_wallet.balance -= amount
            seller_wallet.withdrawn += amount
            seller_wallet.save()
            self.instance = money_withdraw
            return self.instance
