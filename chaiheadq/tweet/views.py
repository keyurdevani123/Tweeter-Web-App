from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Like, Comment, CustomUser, Notification, Message
from .forms import TweetForm, UserRegistrationForm, CommentForm, MessageForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef


User = get_user_model()

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
   # Check if the user is authenticated
    if request.user.is_authenticated:
        for tweet in tweets:
            tweet.liked_by_user = tweet.likes.filter(user=request.user).exists()
    else:
        # If the user is not authenticated, set liked_by_user to False
        for tweet in tweets:
            tweet.liked_by_user = False
    return render(request, 'tweet_list.html', {'tweets': tweets, 'user': request.user})

@csrf_exempt
@login_required
def like_tweet(request, tweet_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        if tweet.user != user:
            Notification.objects.create(user=tweet.user,sender=user,notification_type='like',message=f"{user.username} liked your tweet.",related_tweet=tweet)

    return JsonResponse({
        'liked': liked,
        'likes_count': tweet.likes_count
    })


@login_required
def tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    tweet.views += 1
    tweet.save()

    comments = tweet.comments.all()
    comment_form = CommentForm()

    return render(request, 'tweet_view.html', {
        'tweet': tweet,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def tweet_comments(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = Comment.objects.filter(tweet=tweet).order_by('-created_at')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_comments', tweet_id=tweet.id)
    else:
        form = CommentForm()

    return render(request, 'comments.html', {
        'tweet': tweet,
        'comments': comments,
        'comment_form': form
    })

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required 
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def list_users(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude logged-in user
    return render(request, 'list_users.html', {'users': users})

def user_search(request):
    query = request.GET.get('query', '').strip()
    results = []
    
    if query:
        users = User.objects.filter(username__icontains=query)[:5]  # Limit the number of results
        results = [{"username": user.username, "user_id": user.id, "profile_image": user.user_profile_image.url if user.user_profile_image else "/static/default_profile.png"} for user in users]
        
    return JsonResponse({"results": results})

@login_required
def user_details(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user == request.user:
        followers_count = request.user.followers.count()
        following_count = request.user.following.count()
        followers_list = request.user.followers.all()
        following_list = request.user.following.all()

        context = {
            'user': request.user,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers_list': followers_list,
            'following_list': following_list,
        }

        return render(request, 'logged_user_details.html', context)
    else:
        is_following = target_user.followers.filter(id=request.user.id).exists()
        followers_count = target_user.followers.count()
        following_count = target_user.following.count()

        context = {
            'target_user': target_user,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
        }

        return render(request, 'unlogged_user_details.html', context)


@login_required
def follow(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user != request.user: 
        if target_user.followers.filter(id=request.user.id).exists():
            target_user.followers.remove(request.user)
            followed = False
        else:
            target_user.followers.add(request.user)
            followed = True
            
            Notification.objects.create(user=target_user,sender=request.user,notification_type='follow',message=f"{request.user.username} started following you.")
    
    return redirect('user_details', user_id=user_id)


def create_notification(user, message, related_tweet=None, related_message=None):
    Notification.objects.create(
        user=user,
        message=message,
        related_tweet=related_tweet,
        related_message=related_message
    )


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = {
        "notifications_count": notifications.count(),
        "notifications": [
            {
                "id": n.id,
                "message": n.message,
                "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "notification_type": n.notification_type,
                "related_tweet_id": n.related_tweet.id if n.related_tweet else None,
                "related_message_id": n.related_message.id if n.related_message else None,
            }
            for n in notifications
        ],
    }
    return JsonResponse(data)



@csrf_exempt
@login_required
def mark_all_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"success": "All notifications marked as read"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def notifications_page(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    response = render(request, "notifications.html", {
        "unread_notifications": unread_notifications
    })
    unread_notifications.update(is_read=True)
    return response
    
    

# @login_required
# def send_message(request, recipient_id):
#     recipient = get_object_or_404(User, id=recipient_id)
    
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             try:
#                 content = form.cleaned_data['content']
#                 new_message = Message.objects.create(sender=request.user, recipient=recipient, content=content)
#                 print(f"Creating Notification for {recipient} for message {request.user}")
#                 Notification.objects.create(user=recipient,sender=request.user,notification_type='message',message=f"{request.user.username} sent you a message.",related_message=new_message)
#                 return redirect('get_messages', recipient_id=recipient.id)
#             except Exception as e:
#                 print(f"Error creating notification: {e}")  # Log the error for debugging
#                 return render(request, 'send_message.html', {'form': form, 'recipient': recipient, 'error': 'Failed to send message.'})
#     else:
#         form = MessageForm()

#     return render(request, 'send_message.html', {'form': form, 'recipient': recipient})



@login_required
def get_messages(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    if request.user == recipient:
        return redirect('messages_page')
    
    # Fetch messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by("created_at")

    # Mark messages as read for the recipient
    messages.filter(recipient=request.user, is_read=False).update(is_read=True)

    # Handle AJAX POST requests for sending new messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            new_message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            Notification.objects.create(user=recipient,sender=request.user,notification_type='message',message=f"{request.user.username} sent you a message.",related_message=new_message)
            return JsonResponse({
                'message': new_message.content,
                'created_at': new_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'sender': request.user.username
            })

    return render(request, 'chat.html', {
        'messages': messages,
        'recipient': recipient
    })

@login_required
def messages_page(request):
    logged_user = request.user

    # Fetch all distinct users who exchanged messages with the logged-in user
    users_interacted = User.objects.exclude(id=logged_user.id).filter(
        Q(sent_messages__recipient=logged_user) | Q(received_messages__sender=logged_user)
    ).distinct()

    # Subquery for the latest message timestamp between the logged user and each other user
    latest_message_time = Message.objects.filter(
        Q(sender=OuterRef('pk'), recipient=logged_user) | Q(sender=logged_user, recipient=OuterRef('pk'))
    ).order_by('-created_at').values('created_at')[:1]

    # Annotate each user with the last message time
    users_with_last_message = users_interacted.annotate(
        last_message_time=Subquery(latest_message_time)
    ).order_by('-last_message_time')  # Sort by the most recent message timestamp

    return render(request, 'messages_page.html', {
        'users': users_with_last_message
    })