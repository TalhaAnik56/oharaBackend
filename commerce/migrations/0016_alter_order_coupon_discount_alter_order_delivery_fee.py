# Generated by Django 5.0.1 on 2024-02-08 07:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0015_remove_cart_coupon_discount_remove_cart_delivery_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon_discount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 'Discount can not be less than zero'), django.core.validators.MaxValueValidator(3000, 'Discount can not be greater than 3000')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_fee',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(300, 'Delivery fee can not be greater than 300')]),
        ),
    ]
