# Generated by Django 5.0 on 2024-01-16 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='featuredBook',
        ),
    ]
