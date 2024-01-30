from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("customers", views.CustomerViewSet, basename="customer")
router.register("sellers", views.SellerViewSet, basename="seller")

urlpatterns = router.urls
