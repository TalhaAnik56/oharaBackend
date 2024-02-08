from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from rest_framework import serializers

from community.models import Customer
from warehouse.models import Book, BookItem

from .models import Cart, CartItem, Order, OrderItem


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
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                **self.validated_data, cart_id=cart_id, unit_price=book_item.unit_price
            )
            self.instance = cart_item

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    # jodi amon chai je +1 kore kore quantity barabe ba ai type tahole aita use korte hobe
    # def save(self, **kwargs):
    #     quantity = self.validated_data["quantity"]
    #     cart_item = self.instance
    #     cart_item.quantity += quantity
    #     cart_item.save()
    #     self.instance = cart_item
    #     return self.instance


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
            cart_items = CartItem.objects.filter(cart_id=cart.id)

            items_total_price = sum(
                [item.unit_price * item.quantity for item in cart_items]
            )
            if coupon_discount > items_total_price:
                raise serializers.ValidationError(
                    "Coupon discount cannot be greater than the books' total price"
                )

            order_items = [
                OrderItem(
                    order=order,
                    book_item=item.book_item,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            cart.delete()
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status", "order_status"]
