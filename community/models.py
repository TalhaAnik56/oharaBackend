from django.conf import settings
from django.contrib import admin
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True
    )
    address = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True
    )
    brand_name = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12)
    nid = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return self.brand_name
