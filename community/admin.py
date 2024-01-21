from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['name','address','phone_no','birth_date','joined_at']
    ordering=['name']


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display=['brand_name','address','phone_no','nid','birth_date','joined_at']
    ordering=['brand_name','address']