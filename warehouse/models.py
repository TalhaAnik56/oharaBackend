from django.db import models
from django.core.validators import MaxValueValidator
from community.models import Seller,Customer

# Create your models here.


class Genre(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=1000)
    featured_book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True,related_name='+')

class Writer(models.Model):
    name=models.CharField(max_length=35)
    about=models.CharField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title=models.CharField(max_length=255)
    publication=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    writer=models.ForeignKey(Writer,on_delete=models.PROTECT)
    genre=models.ForeignKey(Genre,on_delete=models.PROTECT)

class BookList(models.Model):
    description=models.CharField(max_length=1500)
    unitPrice=models.DecimalField(max_digits=6,decimal_places=2)
    discountedPrice=models.DecimalField(max_digits=6,decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    seller=models.ForeignKey(Seller,on_delete=models.PROTECT)
    book=models.ForeignKey(Book,on_delete=models.PROTECT)
    

class Feedback(models.Model):
    rating=models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(10, "Rating cannot exceed 10")
        ],null=True)
    comment=models.CharField(max_length=1000)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)