# Generated by Django 5.0.1 on 2024-02-03 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_remove_customer_name_customer_user_seller_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
