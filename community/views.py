from rest_framework.filters import OrderingFilter, SearchFilter
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

        queryset = Customer.objects.all().order_by("name")
        return queryset

    serializer_class = CustomerSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["address", "birth_date", "joined_at"]
    search_fields = ["name", "address"]


class SellerViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = Seller.objects.all().order_by("brand_name")
        return queryset

    serializer_class = SellerSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["brand_name", "nid", "address"]
    ordering_fields = ["address", "joined_at"]
