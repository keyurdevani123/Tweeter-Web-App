from django.shortcuts import render
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/view/', views.tweet_view, name='tweet_view'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    # path('similar/<int:tweet_id>/', views.tweet_similar, name='tweet_similar'),
    path('search/', views.tweet_search, name='tweet_search'),
    path('user/details/', views.user_details, name='user_details'),

    #reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ########################################

    # path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
]