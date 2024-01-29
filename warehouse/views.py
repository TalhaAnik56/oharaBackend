from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
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

# Create your views here.


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all().annotate(book_count=Count("book")).order_by("title")
    serializer_class = GenreSerializer

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        if genre.book_set.count() > 0:
            return Response(
                {
                    "detail": "You have to delete the books first associate with this genre"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        genre.delete()
        return Response(
            {"detail": "The genre has been deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class WriterViewSet(ModelViewSet):
    queryset = Writer.objects.all().annotate(book_count=Count("book")).order_by("name")
    serializer_class = WriterSerializer

    def destroy(self, request, *args, **kwargs):
        writer = get_object_or_404(Writer, pk=kwargs["pk"])
        if writer.book_set.count() > 0:
            return Response(
                {"detail": "You have to delete the books first"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        writer.delete()
        return Response(
            {"detail": "The writer has been deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class BookViewSet(ModelViewSet):
    queryset = (
        Book.objects.all()
        .annotate(
            book_item_count=Count("bookitem", distinct=True),
            feedback_count=Count("feedback", distinct=True),
        )
        .select_related("genre")
        .select_related("writer")
        .order_by("title")
    )
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["pk"])
        if book.bookitem_set.count() > 0:
            return Response(
                {
                    "detail": "You need to delete the book items first associated with this book"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        book.delete()
        return Response(
            {"detail": "The book is deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class BookItemViewSet(ModelViewSet):
    def get_queryset(self):
        return BookItem.objects.filter(book_id=self.kwargs["book_pk"]).select_related(
            "book"
        )

    serializer_class = BookItemSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}


class FeedbackViewSet(ModelViewSet):
    def get_queryset(self):
        return (
            Feedback.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("book")
            .select_related("customer")
        )

    serializer_class = FeedbackSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}
