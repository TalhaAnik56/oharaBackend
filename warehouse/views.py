from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer,WriterSerializer,GenreSerializer
from .models import Book,Writer,Genre

# Create your views here.

@api_view(['GET','POST'])
def genre_list(request):
   if request.method=='GET':
      queryset=Genre.objects.all().annotate(book_count=Count('book')).order_by('title')
      serializer=GenreSerializer(queryset,many=True)
      return Response(serializer.data)
   
   elif request.method=='POST':
      serializer=GenreSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','DELETE'])
def genre_details(request,pk):
   genre=get_object_or_404(Genre.objects.all().annotate(book_count=Count('book')),pk=pk)

   if request.method=='GET':
      serializer=GenreSerializer(genre)
      return Response(serializer.data)
   
   elif request.method=='DELETE':
      if genre.book_set.count()>0:
         return Response({"detail":"You have to delete the books first of this genre"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      genre.delete()
      return Response({"detail":"The genre has been deleted"},status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def writer_list(request):
   if request.method=='GET':
      queryset=Writer.objects.all().annotate(book_count=Count('book')).order_by('name')
      serializer=WriterSerializer(queryset,many=True)
      return Response(serializer.data)
   
   elif request.method=='POST':
      serializer=WriterSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','DELETE'])
def writer_details(request,pk):
   writer=get_object_or_404(Writer.objects.all().annotate(book_count=Count('book')),pk=pk)

   if request.method=='GET':
      serializer=WriterSerializer(writer)
      return Response(serializer.data)
   
   elif request.method=='DELETE':
      if writer.book_set.count()>0:
         return Response({"detail":"You have to delete the books first"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      writer.delete()
      return Response({"detail":"The writer has been deleted."},status=status.HTTP_204_NO_CONTENT)



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

