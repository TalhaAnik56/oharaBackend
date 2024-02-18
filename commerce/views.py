from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from community.models import Customer
from widespread.paginations import CustomPagination
from widespread.permissions import IsAdminOrIsSeller, IsSeller

from .models import Cart, CartItem, MoneyWithdraw, Order, OrderItem, SellerWallet
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CreateOrderSerializer,
    MoneyWithdrawSerializer,
    OrderSerializer,
    OrderSerializerForSeller,
    SellerWalletSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
    UpdateOrderSerializerForSeller,
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
        queryset = (
            Order.objects.prefetch_related(
                "orderitem_set__book_item__book", "orderitem_set__book_item__seller"
            )
            .select_related("customer")
            .all()
        )
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

    pagination_class = CustomPagination


class OrderViewSetForSeller(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    http_method_names = ["get", "patch", "head", "options"]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = (
                Order.objects.prefetch_related(
                    "orderitem_set__book_item__book", "orderitem_set__book_item__seller"
                )
                .select_related("customer")
                .all()
            )
            return queryset
        queryset = (
            Order.objects.filter(orderitem__book_item__seller=self.request.user.seller)
            .select_related("customer")
            .distinct()
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.filter(
                        book_item__seller=self.request.user.seller
                    ).select_related("book_item__book", "book_item__seller"),
                )
            )
            .all()
        )
        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrIsSeller()]
        return [IsSeller()]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateOrderSerializerForSeller
        return OrderSerializerForSeller

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateOrderSerializerForSeller(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializerForSeller(order)
        return Response(serializer.data)

    @action(detail=False)
    def order_due(self, request):
        queryset = self.get_queryset()
        queryset = queryset.exclude(order_status="D")
        serializer = OrderSerializerForSeller(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def order_delivered(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(order_status="D")
        serializer = OrderSerializerForSeller(queryset, many=True)
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
