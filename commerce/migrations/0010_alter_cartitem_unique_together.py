# Generated by Django 5.0.1 on 2024-02-01 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0009_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]
