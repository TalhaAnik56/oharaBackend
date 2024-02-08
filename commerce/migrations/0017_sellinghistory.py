# Generated by Django 5.0.1 on 2024-02-08 14:20

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0016_alter_order_coupon_discount_alter_order_delivery_fee'),
        ('community', '0008_alter_customer_birth_date'),
        ('warehouse', '0015_alter_book_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, "Quantity can't be less than 1")])),
                ('book_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.bookitem')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.order')),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='community.seller')),
            ],
        ),
    ]
