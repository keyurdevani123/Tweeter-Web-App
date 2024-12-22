from django.shortcuts import render
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('<int:tweet_id>/view/', views.tweet_view, name='tweet_view'),
    path('<int:tweet_id>/comments/', views.tweet_comments, name='tweet_comments'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('user_search/', views.user_search, name='user_search'),
    path('user/details/<int:user_id>/', views.user_details, name='user_details'),

    # Connect user functionality
    path('follow/<int:user_id>/', views.follow, name='follow'),
    
    # Notifications
    path("notifications/", views.notifications_page, name="notifications_page"),
    path("notifications/get/", views.get_notifications, name="get_notifications"),
    path('notifications/mark_all_read/<int:notification_id>/', views.mark_all_notifications_as_read, name="mark_all_notifications_as_read"),

    # Message-related paths
    path('messages/', views.messages_page, name='messages_page'),
    # path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('messages/<int:recipient_id>/', views.get_messages, name='get_messages'),

    # Reset password URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
