from django.db import models
from django.core.validators import MaxValueValidator
from warehouse.models import BookItem
from community.models import Seller,Customer


# Create your models here.

class Coupon(models.Model):
    couponCode=models.SlugField(max_length=15)
    discount=models.PositiveSmallIntegerField()
    minimumPurchase=models.PositiveSmallIntegerField()
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    


class Cart(models.Model):
    deliveryFee=models.PositiveSmallIntegerField(default=50)
    couponDiscount=models.PositiveSmallIntegerField(default=0)
    createdAt=models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    bookItem=models.ForeignKey(BookItem,on_delete=models.CASCADE)
    unitPrice=models.PositiveSmallIntegerField()
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

    paymentStatus=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PENDING)
    orderStatus=models.CharField(max_length=1,choices=ORDER_STATUS,default=CONFIRMED)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    deliveryFee=models.PositiveSmallIntegerField()
    coupon_discount=models.PositiveSmallIntegerField()
    createdAt=models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    bookItem=models.ForeignKey(BookItem,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveSmallIntegerField(validators=[MaxValueValidator(30,"You can't order more than 30 pieces")])
    unitPrice=models.PositiveSmallIntegerField()
    order=models.ForeignKey(Order,on_delete=models.CASCADE)


    
        

