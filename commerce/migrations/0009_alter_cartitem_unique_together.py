# Generated by Django 5.0.1 on 2024-02-01 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0008_alter_cart_id'),
        ('warehouse', '0012_feedback_posted_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('book_item', 'cart')},
        ),
    ]