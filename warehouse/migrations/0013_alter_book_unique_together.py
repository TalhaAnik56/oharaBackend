# Generated by Django 5.0.1 on 2024-02-03 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0012_feedback_posted_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('title', 'writer')},
        ),
    ]
