from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer,WriterSerializer,GenreSerializer,FeedbackSerializer
from .models import Book,Writer,Genre,Feedback

# Create your views here.

class GenreList(ListCreateAPIView):
   queryset=Genre.objects.all().annotate(book_count=Count('book')).order_by('title')
   serializer_class=GenreSerializer



class GenreDetails(RetrieveUpdateDestroyAPIView):
   queryset=Genre.objects.all().annotate(book_count=Count('book'))
   serializer_class=GenreSerializer

   def delete(self,request,pk):
      genre=get_object_or_404(self.get_queryset(),pk=pk)
      if genre.book_set.count()>0:
         return Response({"detail":"You have to delete the books first associate with this genre"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      genre.delete()
      return Response({"detail":"The genre has been deleted"},status=status.HTTP_204_NO_CONTENT)
        



class WriterList(ListCreateAPIView):
   queryset=Writer.objects.all().annotate(book_count=Count('book')).order_by('name')
   serializer_class=WriterSerializer



class WriterDetails(RetrieveUpdateDestroyAPIView):
   queryset=Writer.objects.all().annotate(book_count=Count('book')).order_by('name')
   serializer_class=WriterSerializer

   def delete(self,request,pk):
      writer=get_object_or_404(Writer,pk=pk)
      if writer.book_set.count()>0:
         return Response({"detail":"You have to delete the books first"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      writer.delete()
      return Response({"detail":"The writer has been deleted."},status=status.HTTP_204_NO_CONTENT)



class BookList(ListCreateAPIView):
   queryset=Book.objects.all().annotate(book_item_count=Count('bookitem',distinct=True),feedback_count=Count('feedback',distinct=True)).select_related('genre').select_related('writer').order_by('title')
   serializer_class=BookSerializer



class BookDetails(RetrieveUpdateDestroyAPIView):
   queryset=Book.objects.all().annotate(book_item_count=Count('bookitem',distinct=True),feedback_count=Count('feedback',distinct=True)).select_related('genre').select_related('writer').order_by('title')
   serializer_class=BookSerializer

   def delete(self,request,pk):
      book=get_object_or_404(Book,pk=pk)
      if book.bookitem_set.count()>0:
         return Response({"detail":"You need to delete the book items first associated with this book"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      book.delete()
      return Response({"detail":"The book is deleted"},status=status.HTTP_204_NO_CONTENT)
      


@api_view(['GET','POST'])
def feedback_list(request,pk):
   if request.method=='GET':
      queryset=Feedback.objects.all().select_related('book').select_related('customer').filter(book_id=pk)
      serializer=FeedbackSerializer(queryset,many=True)
      return Response(serializer.data)
   
   elif request.method=='POST':
      serializer=FeedbackSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
   

