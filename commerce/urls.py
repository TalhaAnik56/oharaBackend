from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("carts", views.CartViewSet, basename="cart")

urlpatterns = [path("", include(router.urls))]
