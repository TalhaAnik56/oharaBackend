from django.db import models

# Create your models here.


class Genre(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=1000)
    featured_book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True,related_name='+')

class Writer(models.Model):
    name=models.CharField(max_length=35)
    about=models.CharField(max_length=1000)

class Book(models.Model):
    title=models.CharField(max_length=255)
    publication=models.CharField(max_length=25)
    writer=models.ForeignKey(Writer,on_delete=models.PROTECT)
    genre=models.ForeignKey(Genre,on_delete=models.PROTECT)

class BookList(models.Model):
    description=models.TextField()
    unitPrice=models.DecimalField(max_digits=6,decimal_places=2)
    discountedPrice=models.DecimalField(max_digits=6,decimal_places=2)
    stock=models.PositiveIntegerField()
    seller=models.ForeignKey('Seller',on_delete=models.PROTECT)
    book=models.ForeignKey(Book,on_delete=models.PROTECT)

