from django.contrib import admin
from django.db.models import (
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    OuterRef,
    Subquery,
    Sum,
)
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

# Register your models here.


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "book_item",
        "unit_price",
        "quantity",
        "individual_total",
        "order",
    ]
    autocomplete_fields = ["book_item"]
    list_per_page = 10

    def get_queryset(self, request):
        individual_total = ExpressionWrapper(
            F("quantity") * F("unit_price"), output_field=DecimalField()
        )
        return super().get_queryset(request).annotate(individual_total=individual_total)

    def individual_total(self, order_item):
        return order_item.individual_total


class OrderItemTabularInline(admin.TabularInline):
    min_num = 1
    max_num = 20
    extra = 0
    model = models.OrderItem
    autocomplete_fields = ["book_item"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]
    list_display = [
        "id",
        "customer",
        "payment_status",
        "order_status",
        "delivery_address",
        "item_count",
        "delivery_fee",
        "coupon_discount",
        "total_amount",
        "created_at",
    ]
    list_select_related = ["customer"]
    autocomplete_fields = ["customer"]
    search_fields = ["customer__name__istartswith"]
    ordering = ["-created_at"]
    list_per_page = 10

    def get_queryset(self, request):
        # ekhane Sum function e distinct=True use korle same book item koyekta alada alada order er orderItem hishabe thakleo 1 barer beshi
        # count kore na, mane 1 ta order er jonne oi book_item er price count kore,baki order gulate same book item thakleo count kore na,
        # se karone total amount calculation e vul hoy,ai karone distinct=True muche diyechi.

        total_amount = (
            Sum(
                ExpressionWrapper(
                    F("orderitem__quantity") * F("orderitem__unit_price"),
                    output_field=DecimalField(),
                )
            )
            + F("delivery_fee")
            - F("coupon_discount")
        )
        return (
            super()
            .get_queryset(request)
            .annotate(item_count=Count("orderitem"), total_amount=total_amount)
        )

    @admin.display(ordering="item_count")
    def item_count(self, order):
        url = (
            reverse("admin:commerce_orderitem_changelist")
            + "?"
            + urlencode({"order__id": str(order.id)})
        )
        return format_html("<a href={}>{}</a>", url, order.item_count)

    @admin.display(ordering="total_amount")
    def total_amount(self, order):
        return order.total_amount


@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["coupon_code", "discount", "minimum_purchase", "seller"]
    autocomplete_fields = ["seller"]


@admin.register(models.SellerWallet)
class SellerWalletAdmin(admin.ModelAdmin):
    list_display = ["seller", "balance", "withdrawn", "total_earned"]
    autocomplete_fields = ["seller"]
    search_fields = ["seller__brand_name__istartswith"]


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "delivery_fee", "coupon_discount", "created_at"]
