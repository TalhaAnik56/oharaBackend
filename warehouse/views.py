from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .models import Book,Writer

# Create your views here.

@api_view(['GET','POST'])
def book_list(request):
    if request.method=='GET':
      queryset=Book.objects.all().annotate(book_item_count=Count('bookitem')).select_related('genre').select_related('writer').order_by('title')
      serializer=BookSerializer(queryset,many=True)
      return Response(serializer.data)
    
    elif request.method=='POST':
       serializer=BookSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','DELETE'])
def book_details(request,pk):
   book=get_object_or_404(Book,pk=pk)

   if request.method=='GET':
      serializer=BookSerializer(book)
      return Response(serializer.data)
   
   elif request.method=='DELETE':
      if book.bookitem_set.count()>0:
         return Response({"detail":"You need to delete the book items first"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      book.delete()
      return Response({"detail":"The book is deleted"},status=status.HTTP_204_NO_CONTENT)

