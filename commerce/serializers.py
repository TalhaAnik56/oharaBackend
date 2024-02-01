from rest_framework import serializers

from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "delivery_fee", "coupon_discount", "created_at"]

    id = serializers.UUIDField(read_only=True)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["book_item", "unit_price", "quantity", "cart"]

    book_item = serializers.StringRelatedField(read_only=True)


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
            print(cart_item.book_item)
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                **self.validated_data, cart_id=cart_id, unit_price=book_item.unit_price
            )
            self.instance = cart_item

        return self.instance
