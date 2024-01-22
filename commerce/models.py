from django.db import models
from django.core.validators import MaxValueValidator
from warehouse.models import BookItem
from community.models import Seller,Customer


# Create your models here.

class Coupon(models.Model):
    coupon_code=models.SlugField(max_length=15)
    discount=models.PositiveSmallIntegerField()
    minimum_purchase=models.PositiveSmallIntegerField()
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    


class Cart(models.Model):
    delivery_fee=models.PositiveSmallIntegerField(default=50)
    coupon_discount=models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    book_item=models.ForeignKey(BookItem,on_delete=models.CASCADE)
    unit_price=models.PositiveSmallIntegerField()
    quantity=models.PositiveSmallIntegerField(validators=[MaxValueValidator(30,"You can't order more than 30 pieces")])
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)



class Order(models.Model):
    PENDING='P'
    CONFIRMED='C'
    DELIVERED='D'
    RECEIVED='R'
    DELIVERY_ONGOING='O'
    FAILED='F'

    PAYMENT_STATUS=[(PENDING,'pending'),(RECEIVED,'received'),(FAILED,'failed')]
    ORDER_STATUS=[(CONFIRMED,'confirmed'),(DELIVERY_ONGOING,'delivery ongoing'),(DELIVERED,'delivered'),(FAILED,'failed')]

    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PENDING)
    order_status=models.CharField(max_length=1,choices=ORDER_STATUS,default=CONFIRMED)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    delivery_fee=models.PositiveSmallIntegerField()
    delivery_address=models.CharField(max_length=150)
    coupon_discount=models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    book_item=models.ForeignKey(BookItem,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveSmallIntegerField(validators=[MaxValueValidator(30,"You can't order more than 30 pieces")])
    unit_price=models.PositiveSmallIntegerField()
    order=models.ForeignKey(Order,on_delete=models.CASCADE)

class SellerWallet(models.Model):
    balance=models.PositiveIntegerField()
    withdrawn=models.PositiveIntegerField()
    total_amount=models.PositiveIntegerField()
    seller=models.OneToOneField(Seller,on_delete=models.CASCADE,primary_key=True)    
        

