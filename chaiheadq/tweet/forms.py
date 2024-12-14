from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
#from django.conf import settings
#User = settings.AUTH_USER_MODEL
#from .models import CustomUser


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'photo', 'bio')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'photo', 'bio')

