# Generated by Django 5.0.1 on 2024-02-04 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0012_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can Cancel Order')]},
        ),
    ]
