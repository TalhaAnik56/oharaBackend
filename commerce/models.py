from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from community.models import Customer, Seller
from warehouse.models import BookItem

# Create your models here.


class Coupon(models.Model):
    coupon_code = models.SlugField(max_length=15)
    discount = models.PositiveSmallIntegerField()
    minimum_purchase = models.PositiveSmallIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class CartItem(models.Model):
    book_item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    unit_price = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(30, "You can't order more than 30 pieces"),
            MinValueValidator(1, "Quantity should be at least 1"),
        ]
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["book_item", "cart"]]


class Order(models.Model):
    PENDING = "P"
    CONFIRMED = "C"
    DELIVERED = "D"
    RECEIVED = "R"
    DELIVERY_ONGOING = "O"
    # We are using failed instead of cancelled.Because for that we have to use C, but we already have a C for Confirmed.
    FAILED = "F"

    PAYMENT_STATUS = [(PENDING, "pending"), (RECEIVED, "received")]
    ORDER_STATUS = [
        (PENDING, "pending"),
        (CONFIRMED, "confirmed"),
        (DELIVERY_ONGOING, "delivery ongoing"),
        (DELIVERED, "delivered"),
        (FAILED, "failed"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PENDING
    )
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default=PENDING)
    delivery_fee = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(300, "Delivery fee can not be greater than 300"),
        ],
    )
    delivery_address = models.CharField(max_length=200)
    coupon_discount = models.PositiveSmallIntegerField(default=0)
    money_transferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        permissions = [("cancel_order", "Can Cancel Order")]


class OrderItem(models.Model):
    book_item = models.ForeignKey(BookItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(30, "You can't order more than 30 pieces")]
    )
    unit_price = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    confirmed_by_seller = models.BooleanField(default=False)
    transferred_to_inventory = models.BooleanField(default=False)


class SellerWallet(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, unique=True)
    balance = models.PositiveIntegerField(null=True, blank=True, default=0)
    withdrawn = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_earned = models.PositiveIntegerField(null=True, blank=True, default=0)
    last_update = models.DateTimeField(auto_now=True)


class MoneyWithdraw(models.Model):
    BKASH = "B"
    NAGAD = "N"
    PAYMENT_METHOD_CHOICES = [(BKASH, "Bkash"), (NAGAD, "Nagad")]

    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(20, "You can't withdraw less than 20 taka"),
            MaxValueValidator(20000, "You can't withdraw more than 20000 taka"),
        ]
    )
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES)
    payment_account_no = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
