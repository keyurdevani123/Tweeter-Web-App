# Generated by Django 5.1.4 on 2024-12-18 07:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0007_connection_deleted_at_connection_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]