from django.contrib import admin
from .models import Tweet
from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser
#from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

admin.site.register(Tweet)

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('photo', 'bio', 'following')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('photo', 'bio')}),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)
