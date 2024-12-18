from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, default='')
    user_bio = models.CharField(max_length=50, default='')
    user_profile_image = models.ImageField(upload_to="profile", default='')
    followers_count = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=180)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)  # Tracks the number of views

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def liked_by_users(self):
        return self.likes.values_list('user__username', flat=True)

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
        return f'Comment by {self.user.username} on {self.tweet}'

class Connection(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_connections')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} follows {self.receiver.username}"

    def unfollow(self):
        self.status = False
        self.save()

    def follow(self):
        self.status = True
        self.save()
