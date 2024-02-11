from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from community.models import Customer
from widespread.permissions import IsAdminOrIsSeller

from .models import Cart, CartItem, MoneyWithdraw, Order, SellerWallet
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CreateOrderSerializer,
    MoneyWithdrawSerializer,
    OrderSerializer,
    SellerWalletSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
)

# Create your views here.


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = (
        Cart.objects.all()
        .prefetch_related("cartitem_set__book_item__seller")
        .prefetch_related("cartitem_set__book_item__book")
    )
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

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
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


class OrderViewSet(ModelViewSet):

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.prefetch_related(
            "orderitem_set__book_item__book", "orderitem_set__book_item__seller"
        ).all()
        if user.is_staff:
            return queryset
        customer = Customer.objects.get(user_id=user.id)
        return queryset.filter(customer_id=customer.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class SellerWalletViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = SellerWallet.objects.select_related("seller").all()
        if user.is_staff:
            return queryset
        return queryset.filter(seller=user.seller)

    serializer_class = SellerWalletSerializer
    permission_classes = [IsAdminOrIsSeller]


class MoneyWithdrawViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    def get_queryset(self):
        queryset = MoneyWithdraw.objects.select_related("seller").all()
        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(seller=user.seller)

    serializer_class = MoneyWithdrawSerializer
    permission_classes = [IsAdminOrIsSeller]

    def get_serializer_context(self):
        return {"seller_id": self.request.user.seller.id}
