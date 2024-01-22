# Generated by Django 5.0 on 2024-01-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_rename_coupondiscount_cart_coupon_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerwallet',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='sellerwallet',
            name='total_earned',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='sellerwallet',
            name='balance',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='sellerwallet',
            name='withdrawn',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
