from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Connection

@receiver(post_save, sender=Connection)
def update_followers_count(sender, instance, created, **kwargs):
    if created or instance.status:  # Created or status restored
        instance.receiver.followers_count = Connection.objects.filter(receiver=instance.receiver, status=True).count()
        instance.receiver.save()

@receiver(pre_delete, sender=Connection)
def decrement_followers_count(sender, instance, **kwargs):
    instance.receiver.followers_count = Connection.objects.filter(receiver=instance.receiver, status=True).count()
    instance.receiver.save()
