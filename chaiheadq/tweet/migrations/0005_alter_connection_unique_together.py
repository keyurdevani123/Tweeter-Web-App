# Generated by Django 5.1.4 on 2024-12-17 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0004_connection'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together=set(),
        ),
    ]
