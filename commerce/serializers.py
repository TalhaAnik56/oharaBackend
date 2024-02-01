from rest_framework import serializers

from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "delivery_fee", "coupon_discount", "created_at"]

    id = serializers.UUIDField(read_only=True)
