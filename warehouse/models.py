from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from community.models import Customer, Seller

# Create your models here.


class Genre(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    featured_book = models.ForeignKey(
        "Book", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    def __str__(self):
        return self.title


class Writer(models.Model):
    name = models.CharField(max_length=35, unique=True)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    publication = models.CharField(max_length=25)
    writer = models.ForeignKey(Writer, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    description = models.CharField(max_length=1500)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.title + "--" + self.seller.brand_name

    class Meta:
        unique_together = ["book", "seller"]


class Feedback(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(1, "Rating cannot be less than 1"),
            MaxValueValidator(10, "Rating cannot exceed 10"),
        ],
        null=True,
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
