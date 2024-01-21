from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import urlencode,format_html
from . import models

#admin er name:admin,password:talha

# Register your models here.

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display=['title','description','featured_book','book_count']
    ordering=['title']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_count=Count('book'))

    @admin.display(ordering='book_count')
    def book_count(self,genre):
        url=reverse('admin:warehouse_book_changelist') + '?' + urlencode({'genre__id':str(genre.id)})
        print(url)
        return format_html('<a href={}>{}</a>',url,genre.book_count)
    


@admin.register(models.Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display=['name','about','created_at','book_count']
    ordering=['name']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(book_count=Count('book'))
    
    @admin.display(ordering='book_count')
    def book_count(self,writer):
        url=reverse('admin:warehouse_book_changelist')+'?'+urlencode({'writer__id':str(writer.id)})
        return format_html('<a href={}>{}</a>',url,writer.book_count)



@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['title','publication','writer','genre','created_at']
    ordering=['title']



@admin.register(models.BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display=['book','seller','description','unit_price','stock','created_at']