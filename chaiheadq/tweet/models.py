from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.timezone import now


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, default='', blank=True)
    user_bio = models.CharField(max_length=150, default='', blank=True)
    user_profile_image = models.ImageField(upload_to="profile/", default='default_profile.png')
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following", blank=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def follow(self, user):
        if not self.followers.filter(id=user.id).exists():
            self.followers.add(user)

    def unfollow(self, user):
        if self.followers.filter(id=user.id).exists():
            self.followers.remove(user)

    def is_following(self, user):
        return self.followers.filter(id=user.id).exists()

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tweets")
    text = models.CharField(max_length=280)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, default='default_photo.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f'{self.user.username} liked {self.tweet.text[:50]}'


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.tweet.text[:50]}'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    related_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']
