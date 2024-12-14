from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=180)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'

# class CustomUser(AbstractUser):
#     photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

#     def __str__(self):
#         return self.username
