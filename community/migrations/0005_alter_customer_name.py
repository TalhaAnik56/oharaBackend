# Generated by Django 5.0 on 2024-01-23 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_rename_birthdate_customer_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
