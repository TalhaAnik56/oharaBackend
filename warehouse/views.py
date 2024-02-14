from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from widespread.paginations import CustomPagination
from widespread.permissions import IsAdminOrIsSeller, IsSeller

from .models import Book, BookItem, Feedback, Genre, Writer
from .serializers import (
    BookItemSerializer,
    BookSerializer,
    CreateBookItemSerializerOnlyForSeller,
    FeedbackSerializer,
    GenreSerializer,
    UpdateBookItemSerializer,
    WriterSerializer,
)


class GenreViewSet(ModelViewSet):
    queryset = (
        Genre.objects.all()
        .select_related("featured_book")
        .annotate(book_count=Count("book"))
        .order_by("title")
    )
    serializer_class = GenreSerializer

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, pk=kwargs["pk"])
        if genre.book_set.count() > 0:
            return Response(
                {
                    "detail": "You have to delete the books first associated with this genre"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class WriterViewSet(ModelViewSet):
    queryset = Writer.objects.all().annotate(book_count=Count("book")).order_by("name")
    serializer_class = WriterSerializer

    def destroy(self, request, *args, **kwargs):
        writer = get_object_or_404(Writer, pk=kwargs["pk"])
        if writer.book_set.count() > 0:
            return Response(
                {
                    "detail:You have to delete the books first associated with this writer"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class BookViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = (
            Book.objects.all()
            .select_related("writer")
            .select_related("genre")
            .annotate(book_item_count=Count("bookitem", distinct=True))
            .annotate(feedback_count=Count("feedback", distinct=True))
            .order_by("title")
        )

        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrIsSeller()]

        elif self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]

        return [AllowAny()]

    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["genre", "writer"]
    search_fields = ["title", "writer__name", "genre__title"]
    ordering_fields = ["created_at"]

    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["pk"])
        if book.bookitem_set.count() > 0:
            return Response(
                {
                    "detail:You have to delete the book items first associated with this book"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class BookItemViewSetForSeller(ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]

    def get_queryset(self):
        seller = self.request.user.seller
        queryset = (
            BookItem.objects.filter(seller=seller)
            .select_related("book")
            .select_related("seller")
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateBookItemSerializer
        elif self.request.method == "POST":
            return CreateBookItemSerializerOnlyForSeller
        else:
            return BookItemSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        does_exist = BookItem.objects.filter(
            pk=instance.id, seller=user.seller
        ).exists()

        if does_exist:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "error": "This is not your book item. You can't update or delete this"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    pagination_class = CustomPagination
    permission_classes = [IsSeller]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["unit_price", "stock"]
    search_fields = ["book__title", "book__writer__name"]


class BookItemViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]

    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = (
            BookItem.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("book__writer")
            .select_related("book__genre")
            .select_related("seller")
            .order_by("book__title")
        )
        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSeller()]
        elif self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrIsSeller()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateBookItemSerializer
        return BookItemSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"], "user": self.request.user}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        does_exist = BookItem.objects.filter(
            pk=instance.id, seller=user.seller
        ).exists()

        if user.is_staff or does_exist:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "error": "This is not your book item. You can't update or delete this"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["unit_price", "stock"]


class FeedbackViewSet(ModelViewSet):
    def get_queryset(self):
        page_size = self.request.query_params.get("page_size")

        if page_size is not None:
            CustomPagination.page_size = page_size
            self.pagination_class = CustomPagination

        queryset = (
            Feedback.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("customer__user")
            .select_related("book")
            .order_by("book__title")
        )
        return queryset

    serializer_class = FeedbackSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}
