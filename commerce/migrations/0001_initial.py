# Generated by Django 5.0.1 on 2024-02-10 11:56

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0008_alter_customer_birth_date'),
        ('warehouse', '0015_alter_book_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SellerWallet',
            fields=[
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='community.seller')),
                ('balance', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('withdrawn', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_earned', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.SlugField(max_length=15)),
                ('discount', models.PositiveSmallIntegerField()),
                ('minimum_purchase', models.PositiveSmallIntegerField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('P', 'pending'), ('R', 'received')], default='P', max_length=1)),
                ('order_status', models.CharField(choices=[('C', 'confirmed'), ('O', 'delivery ongoing'), ('D', 'delivered'), ('F', 'failed')], default='C', max_length=1)),
                ('delivery_fee', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(300, 'Delivery fee can not be greater than 300')])),
                ('delivery_address', models.CharField(max_length=200)),
                ('coupon_discount', models.PositiveSmallIntegerField(default=0)),
                ('money_transferred', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='community.customer')),
            ],
            options={
                'permissions': [('cancel_order', 'Can Cancel Order')],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(30, "You can't order more than 30 pieces")])),
                ('unit_price', models.PositiveSmallIntegerField()),
                ('book_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.bookitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.order')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.PositiveSmallIntegerField()),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(30, "You can't order more than 30 pieces"), django.core.validators.MinValueValidator(1, 'Quantity should be at least 1')])),
                ('book_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.bookitem')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.cart')),
            ],
            options={
                'unique_together': {('book_item', 'cart')},
            },
        ),
    ]
