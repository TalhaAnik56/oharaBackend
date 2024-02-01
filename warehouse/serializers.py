from rest_framework import serializers

from .models import Book, BookItem, Feedback, Genre, Writer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publication",
            "writer",
            "genre",
            "created_at",
            "book_item_count",
            "feedback_count",
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

    book = BookSerializer(read_only=True)

    def to_representation(self, book_item):
        representation = super().to_representation(book_item)
        representation["seller"] = book_item.seller.brand_name
        return representation

    def create(self, validated_data):
        book_id = self.context["book_id"]
        seller = validated_data["seller"]

        book_item, created = BookItem.objects.get_or_create(
            book_id=book_id, seller=seller, defaults=validated_data
        )

        if not created:
            raise serializers.ValidationError(
                "This book and seller combination already exists."
            )

        return book_item


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "title", "description", "featured_book", "book_count"]

    book_count = serializers.IntegerField(read_only=True)

    def to_representation(self, genre):
        representation = super().to_representation(genre)
        if representation["featured_book"] is not None:
            representation["featured_book"] = {
                "title": genre.featured_book.title,
                "publication": genre.featured_book.publication,
            }
        return representation


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ["id", "name", "about", "created_at", "book_count"]

    book_count = serializers.IntegerField(read_only=True)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "book", "comment", "rating", "customer", "posted_at"]

    book = serializers.StringRelatedField(read_only=True)

    def to_representation(self, feedback):
        representation = super().to_representation(feedback)
        representation["customer"] = feedback.customer.name
        return representation

    def create(self, validated_data):
        book_id = self.context["book_id"]
        feedback = Feedback.objects.create(**validated_data, book_id=book_id)
        return feedback
