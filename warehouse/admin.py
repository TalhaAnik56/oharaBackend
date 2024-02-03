from typing import Any

from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

# admin er name:admin,password:1234
# Register your models here.


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "featured_book", "book_count"]
    search_fields = ["title__istartswith"]
    ordering = ["title"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_count=Count("book"))

    @admin.display(ordering="book_count")
    def book_count(self, genre):
        url = (
            reverse("admin:warehouse_book_changelist")
            + "?"
            + urlencode({"genre__id": str(genre.id)})
        )
        print(url)
        return format_html("<a href={}>{}</a>", url, genre.book_count)


@admin.register(models.Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ["name", "about", "created_at", "book_count"]
    search_fields = ["name__istartswith"]
    ordering = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_count=Count("book"))

    @admin.display(ordering="book_count")
    def book_count(self, writer):
        url = (
            reverse("admin:warehouse_book_changelist")
            + "?"
            + urlencode({"writer__id": str(writer.id)})
        )
        return format_html("<a href={}>{}</a>", url, writer.book_count)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "publication",
        "writer",
        "genre",
        "created_at",
        "book_item_count",
        "feedback_count",
    ]
    ordering = ["title"]
    search_fields = ["title__istartswith"]
    autocomplete_fields = ["writer", "genre"]
    list_per_page = 10

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                book_item_count=Count("bookitem", distinct=True),
                feedback_count=Count("feedback", distinct=True),
            )
        )

    @admin.display(ordering="book_item_count")
    def book_item_count(self, book):
        url = (
            reverse("admin:warehouse_bookitem_changelist")
            + "?"
            + urlencode({"book__id": str(book.id)})
        )
        return format_html('<a href="{}">{}</a>', url, book.book_item_count)

    @admin.display(ordering="feedback_count")
    def feedback_count(self, book):
        url = (
            reverse("admin:warehouse_feedback_changelist")
            + "?"
            + urlencode({"book__id": str(book.id)})
        )
        return format_html('<a href="{}">{}</a>', url, book.feedback_count)


class StockFilter(admin.SimpleListFilter):
    title = "Stock"
    parameter_name = "stock"

    def lookups(self, request, model_admin):
        return [("<=10", "Low"), ("<=30", "Medium"), (">=31", "High")]

    def queryset(self, request, queryset):
        if self.value() == "<=10":
            return queryset.filter(stock__lte=10)
        elif self.value() == "<=30":
            return queryset.filter(stock__gt=10, stock__lte=30)
        elif self.value() == ">=31":
            return queryset.filter(stock__gte=31)


@admin.register(models.BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "book",
        "seller",
        "description",
        "unit_price",
        "stock",
        "created_at",
    ]
    autocomplete_fields = ["book", "seller"]
    list_select_related = ["book"]
    search_fields = ["book__title"]
    ordering = ["book__title"]
    list_filter = ["created_at", StockFilter]
    list_per_page = 10


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["book", "comment", "rating", "customer"]
    ordering = ["book"]
    autocomplete_fields = ["book", "customer"]
    list_per_page = 10
