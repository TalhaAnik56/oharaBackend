from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['name','address','phoneNo','birthDate','joinedAt']
    ordering=['name']


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display=['brandName','address','phoneNo','nid','birthDate','joinedAt']
    ordering=['brandName','address']