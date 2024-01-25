from rest_framework import serializers
from .models import Writer,Book,Genre



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','title','publication','writer','genre','book_item_count','created_at',]
        
    book_item_count=serializers.IntegerField(read_only=True)

    def to_representation(self, book):
        representation = super().to_representation(book)
        representation['writer'] = book.writer.name
        representation['genre']=book.genre.title
        return representation
    