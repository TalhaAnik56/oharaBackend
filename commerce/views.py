from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer

# Create your views here.


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = (
            CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
            .select_related("book_item__book")
            .select_related("book_item__seller")
        )

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}
