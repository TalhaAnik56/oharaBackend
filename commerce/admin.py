from typing import Any
from django.contrib import admin
from django.db.models import Count,F,ExpressionWrapper,DecimalField
from django.urls import reverse
from django.utils.html import urlencode,format_html
from . import models

# Register your models here.

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['book_item','unit_price','quantity','individual_total','order',]
    autocomplete_fields=['book_item']

    def get_queryset(self, request):
        individual_total=ExpressionWrapper(F('quantity')*F('unit_price'),output_field=DecimalField())
        return super().get_queryset(request).annotate(individual_total=individual_total)
    
    def individual_total(self,order_item):
        return order_item.individual_total




class OrderItemTabularInline(admin.TabularInline):
    min_num=1
    max_num=20
    extra=0
    model=models.OrderItem
    autocomplete_fields=['book_item']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTabularInline]
    list_display=['id','customer','payment_status',
                  'order_status','delivery_fee',
                  'delivery_address','coupon_discount',
                  'item_count','created_at'
                  ]
    list_select_related=['customer']
    autocomplete_fields=['customer']
    search_fields=['customer__name__istartswith']
    ordering=['-created_at']
    list_per_page=10


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(item_count=Count('orderitem'))
    
    
    @admin.display(ordering='item_count')
    def item_count(self,order):
        url=reverse('admin:commerce_orderitem_changelist')+'?'+urlencode({'order__id':str(order.id)})
        return format_html('<a href={}>{}</a>',url,order.item_count)