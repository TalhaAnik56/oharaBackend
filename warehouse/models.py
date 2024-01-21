from django.db import models
from django.core.validators import MaxValueValidator
from community.models import Seller,Customer

# Create your models here.


class Genre(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=1000)
    featuredBook=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True,blank=True,related_name='+')

    def __str__(self):
        return self.title



class Writer(models.Model):
    name=models.CharField(max_length=35)
    about=models.CharField(max_length=1000)
    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title=models.CharField(max_length=255)
    publication=models.CharField(max_length=25)
    writer=models.ForeignKey(Writer,on_delete=models.PROTECT)
    genre=models.ForeignKey(Genre,on_delete=models.PROTECT)
    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class BookItem(models.Model):
    book=models.ForeignKey(Book,on_delete=models.PROTECT)
    seller=models.ForeignKey(Seller,on_delete=models.PROTECT)
    description=models.CharField(max_length=1500)
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    stock=models.PositiveIntegerField()
    createdAt=models.DateTimeField(auto_now_add=True)
   
    
    def __str__(self):
        return self.book.title
    
    

class Feedback(models.Model):
    rating=models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(10, "Rating cannot exceed 10")
        ],null=True)
    comment=models.CharField(max_length=1000)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
    