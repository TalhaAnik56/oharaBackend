from django.db import models


class Customer(models.Model):
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    phone_no=models.CharField(max_length=12)
    birth_date=models.DateField(null=True)
    joined_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Seller(models.Model):
    brand_name=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    phone_no=models.CharField(max_length=12)
    nid=models.CharField(max_length=30)
    birth_date=models.DateField(null=True)
    joined_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.brand_name




