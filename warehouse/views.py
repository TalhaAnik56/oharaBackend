from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Book, BookItem, Feedback, Genre, Writer
from .serializers import (
    BookItemSerializer,
    BookSerializer,
    FeedbackSerializer,
    GenreSerializer,
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
    queryset = (
        Book.objects.all()
        .select_related("writer")
        .select_related("genre")
        .annotate(book_item_count=Count("bookitem", distinct=True))
        .annotate(feedback_count=Count("feedback", distinct=True))
        .order_by("title")
    )
    serializer_class = BookSerializer

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


class BookItemViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = (
            BookItem.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("book__writer")
            .select_related("book__genre")
            .select_related("seller")
            .order_by("book__title")
        )
        return queryset

    serializer_class = BookItemSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}


class FeedbackViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = (
            Feedback.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("book")
            .select_related("customer")
            .order_by("book__title")
        )
        return queryset

    serializer_class = FeedbackSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}
