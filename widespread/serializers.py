from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_customer",
            "is_seller",
        ]

    is_customer = serializers.SerializerMethodField(
        method_name="check_customer", read_only=True
    )
    is_seller = serializers.SerializerMethodField(
        method_name="check_seller", read_only=True
    )

    def check_customer(self, user):
        if hasattr(user, "customer"):
            return True
        return False

    def check_seller(self, user):
        if hasattr(user, "seller"):
            return True
        return False
