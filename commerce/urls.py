from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register("carts", views.CartViewSet, basename="cart")
router.register("orders", views.OrderViewSet, basename="order")
router.register("sellerwallets", views.SellerWalletViewSet, basename="seller-wallet")
router.register("moneywithdraw", views.MoneyWithdrawViewSet, basename="money-withdraw")

cart_item_router = NestedDefaultRouter(router, "carts", lookup="cart")
cart_item_router.register("cartitems", views.CartItemViewSet, basename="cart-item")

urlpatterns = [path("", include(router.urls)), path("", include(cart_item_router.urls))]
