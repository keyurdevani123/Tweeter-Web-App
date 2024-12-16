from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django.contrib.auth import get_user_model

# User= get_user_model()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number= models.CharField(max_length=100,default='')
    user_bio = models.CharField(max_length=50,default='')
    user_profile_image= models.ImageField(upload_to="profile",default='')

    REQUIRED_FIELDS=['email']
    USERNAME_FIELD = 'username' 

class Tweet(models.Model):
    user = models.ForeignKey('tweet.CustomUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=180)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'


