from rest_framework import serializers
from .models import Writer,Book,Genre,Feedback


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields=['id','title','description','featured_book','book_count']

    book_count=serializers.IntegerField(read_only=True)



class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Writer
        fields=['id','name','about','created_at','book_count']

    book_count=serializers.IntegerField(read_only=True)    



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','title','publication','writer','genre','book_item_count','created_at',]

    book_item_count=serializers.IntegerField(read_only=True)

    def to_representation(self, book):
        representation = super().to_representation(book)
        representation['writer'] = book.writer.name
        representation['genre'] = book.genre.title
        return representation
    


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=['id','book','comment','rating','customer']

    def to_representation(self, feedback):
        representation = super().to_representation(feedback)
        representation['book']=feedback.book.title
        representation['customer']=feedback.customer.name
        return representation
            