# Generated by Django 5.0.1 on 2024-02-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0014_alter_order_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon_discount',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='delivery_fee',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=200),
        ),
    ]