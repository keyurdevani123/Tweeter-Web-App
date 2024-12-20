from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CustomUser, Tweet, Notification


@receiver(post_save, sender=CustomUser)
def update_followers_count(sender, instance, created, **kwargs):
    """Update the followers count when a user is created or their followers change."""
    if created or instance.followers.count() != instance.followers_count:
        instance.followers_count = instance.followers.count()
        instance.save()

@receiver(pre_delete, sender=CustomUser)
def decrement_followers_count(sender, instance, **kwargs):
    """Ensure the followers count is updated when a user is deleted."""
    instance.followers_count = instance.followers.count() - 1
    instance.save()


@receiver(post_save, sender=Tweet)
def create_notification(sender, instance, created, **kwargs):
    if created:
        tweet_author = instance.user
        # Get followers of the tweet author
        followers = tweet_author.followers.all()  # Assuming a ManyToManyField "followers" exists on CustomUser
        for follower in followers:
            Notification.objects.create(
                user=follower,
                message=f"{tweet_author.username} posted a new tweet: {instance.text[:50]}",
                related_tweet=instance
            )
