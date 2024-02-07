from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from widespread.paginations import CustomPagination

from .models import Customer, Seller
from .serializers import CustomerSerializer, SellerSerializer

# Create your views here.


class CustomerViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = (
            Customer.objects.all()
            .select_related("user")
            .order_by("user__first_name", "user__last_name")
        )
        return queryset

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    serializer_class = CustomerSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["address", "birth_date", "joined_at"]
    search_fields = ["user__first_name", "user__last_name"]

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        user = request.user
        (customer, created) = Customer.objects.get_or_create(user_id=user.id)

        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SellerViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = Seller.objects.all().select_related("user").order_by("brand_name")
        return queryset

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    serializer_class = SellerSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["brand_name", "user__first_name", "user__last_name"]
    ordering_fields = ["address", "joined_at"]
