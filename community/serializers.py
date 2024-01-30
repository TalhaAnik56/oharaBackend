from rest_framework import serializers

from .models import Customer, Seller


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "address", "phone_no", "birth_date", "joined_at"]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "brand_name", "phone_no", "nid", "birth_date", "joined_at"]
