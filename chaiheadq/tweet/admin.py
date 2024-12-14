from django.contrib import admin
from .models import Tweet,CustomUser
from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser
#from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

admin.site.register(Tweet)

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'photo', 'bio')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'photo', 'bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'photo', 'bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'              )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
