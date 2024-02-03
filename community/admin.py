from typing import Any

from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "address",
        "phone_no",
        "birth_date",
        "joined_at",
        "feedback_given",
        "order_count",
    ]
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]
    # ai ordering use hocche shurutei kivabe ordering kora hobe tar jonne, ar class er moddhe je ordering kora ache sheita oi field e click kore ordering korar jonne,jemon first_name
    ordering = ["user__first_name", "user__last_name"]
    list_per_page = 10
    list_select_related = ["user"]
    autocomplete_fields = ["user"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                feedback_given=Count("feedback", distinct=True),
                order_count=Count("order", distinct=True),
            )
        )

    @admin.display(ordering="feedback_given")
    def feedback_given(self, customer):
        url = (
            reverse("admin:warehouse_feedback_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.feedback_given)

    @admin.display(ordering="order_count")
    def order_count(self, customer):
        url = (
            reverse("admin:commerce_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.order_count)


class BookCountFilter(admin.SimpleListFilter):
    title = "Book Count"
    parameter_name = "book_count"

    def lookups(self, request, model_admin):
        return [("<=20", "Low"), ("<=50", "Medium"), (">=51", "High")]

    def queryset(self, request, queryset):
        if self.value() == "<=20":
            return queryset.filter(book_count__lte=20)
        elif self.value() == "<=50":
            return queryset.filter(book_count__gt=20, book_count__lte=50)
        elif self.value() == ">=51":
            return queryset.filter(book_count__gte=51)


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "brand_name",
        "address",
        "phone_no",
        "nid",
        "birth_date",
        "joined_at",
        "book_count",
    ]
    search_fields = [
        "brand_name",
        "user__first_name",
        "user__last_name",
    ]
    autocomplete_fields = ["user"]
    ordering = ["user__first_name", "user__last_name", "brand_name"]
    list_filter = [BookCountFilter]
    list_select_related = ["user"]
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_count=Count("bookitem"))

    @admin.display(ordering="book_count")
    def book_count(self, seller):
        url = (
            reverse("admin:warehouse_bookitem_changelist")
            + "?"
            + urlencode({"seller__id": str(seller.id)})
        )
        return format_html("<a href={}>{}</a>", url, seller.book_count)
