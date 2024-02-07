from rest_framework import serializers

from .models import Customer, Seller


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "address",
            "phone_no",
            "birth_date",
            "joined_at",
        ]

    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context["user_id"]
        customer = Customer.objects.create(**validated_data, user_id=user_id)
        return customer


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

    def create(self, validated_data):
        user_id = self.context["user_id"]
        seller = Seller.objects.create(**validated_data, user_id=user_id)
        return seller
