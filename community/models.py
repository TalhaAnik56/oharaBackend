from django.db import models


class Customer(models.Model):
    name=models.CharField(max_length=10)
    address=models.CharField(max_length=50)
    phoneNo=models.CharField(max_length=12)
    birthDate=models.DateField(null=True)
    joined_at=models.DateTimeField(auto_now_add=True)


class Seller(models.Model):
    brandName=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    nid=models.CharField(max_length=30)
    birthDate=models.DateField(null=True)
    joined_at=models.DateTimeField(auto_now_add=True)




