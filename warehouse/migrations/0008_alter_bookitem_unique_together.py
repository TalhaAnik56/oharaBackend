# Generated by Django 5.0 on 2024-01-21 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_rename_birthdate_customer_birth_date_and_more'),
        ('warehouse', '0007_rename_createdat_book_created_at_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookitem',
            unique_together={('book', 'seller')},
        ),
    ]
