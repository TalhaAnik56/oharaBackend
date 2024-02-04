# Generated by Django 5.0.1 on 2024-02-01 02:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0007_alter_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]