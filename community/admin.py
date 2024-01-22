from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['name','address','phone_no','birth_date','joined_at','feedback_given']
    search_fields=['name__istartswith']
    ordering=['name']
    list_per_page=10
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(feedback_given=Count('feedback'))
    
    @admin.display(ordering='feedback_given')
    def feedback_given(self,customer):
        url=reverse('admin:warehouse_feedback_changelist')+'?'+urlencode({'customer__id':str(customer.id)})
        return format_html('<a href="{}">{}</a>',url,customer.feedback_given)


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display=['brand_name','address','phone_no','nid','birth_date','joined_at','book_count']
    search_fields=['brand_name__istartswith']
    ordering=['brand_name','address']
    list_per_page=10
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_count=Count('bookitem'))

    @admin.display(ordering='book_count')
    def book_count(self,seller):
        url=reverse('admin:warehouse_bookitem_changelist')+'?'+urlencode({'seller__id':str(seller.id)})
        return format_html('<a href={}>{}</a>',url,seller.book_count)