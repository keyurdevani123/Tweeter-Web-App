# Generated by Django 5.1.4 on 2024-12-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]