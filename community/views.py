from rest_framework.viewsets import ModelViewSet

from .models import Customer, Seller
from .paginations import CustomPagination
from .serializers import CustomerSerializer, SellerSerializer

# Create your views here.


class CustomerViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = Customer.objects.all()
        return queryset

    serializer_class = CustomerSerializer
    pagination_class = CustomPagination


class SellerViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = Seller.objects.all()
        return queryset

    serializer_class = SellerSerializer
    pagination_class = CustomPagination
