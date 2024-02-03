from rest_framework import serializers

from .models import Customer, Seller


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone_no",
            "birth_date",
            "joined_at",
        ]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "id",
            "first_name",
            "last_name",
            "brand_name",
            "address",
            "phone_no",
            "nid",
            "birth_date",
            "joined_at",
        ]
