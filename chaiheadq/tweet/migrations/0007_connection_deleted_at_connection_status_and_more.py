# Generated by Django 5.1.4 on 2024-12-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0006_tweet_views_comment_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='connection',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together={('sender', 'receiver')},
        ),
    ]
