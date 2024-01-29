from rest_framework import serializers

from .models import Book, BookItem, Feedback, Genre, Writer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "title", "description", "featured_book", "book_count"]

    book_count = serializers.IntegerField(read_only=True)


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ["id", "name", "about", "created_at", "book_count"]

    book_count = serializers.IntegerField(read_only=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publication",
            "writer",
            "genre",
            "book_item_count",
            "feedback_count",
            "created_at",
        ]

    book_item_count = serializers.IntegerField(read_only=True)
    feedback_count = serializers.IntegerField(read_only=True)

    def to_representation(self, book):
        representation = super().to_representation(book)
        representation["writer"] = book.writer.name
        representation["genre"] = book.genre.title
        return representation


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = [
            "id",
            "book",
            "seller",
            "description",
            "unit_price",
            "stock",
            "created_at",
        ]

    book = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        book_id = self.context["book_id"]
        book_item = BookItem.objects.create(book_id=book_id, **validated_data)
        return book_item


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "book", "comment", "rating", "customer"]

    def to_representation(self, feedback):
        representation = super().to_representation(feedback)
        representation["customer"] = feedback.customer.name
        return representation

    book = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        book_id = self.context["book_id"]
        feedback = Feedback.objects.create(book_id=book_id, **validated_data)
        return feedback
