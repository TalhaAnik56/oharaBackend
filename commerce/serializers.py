from rest_framework import serializers

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
            "delivery_fee",
            "coupon_discount",
            "created_at",
            "cartitem_set",
            "total_price",
        ]

    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name="calculated_price", read_only=True
    )

    def calculated_price(self, cart: Cart):
        prices = [
            item.book_item.unit_price * item.quantity
            for item in cart.cartitem_set.all()
        ]
        total = sum(prices) + cart.delivery_fee - cart.coupon_discount
        return total


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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "customer",
            "payment_status",
            "order_status",
            "delivery_fee",
            "coupon_discount",
            "delivery_address",
            "created_at",
        ]
