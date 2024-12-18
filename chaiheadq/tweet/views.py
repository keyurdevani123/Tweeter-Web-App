from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Connection, Like, Comment
from .forms import TweetForm, UserRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,get_user_model
from django.http import JsonResponse
from .forms import CommentForm
from .models import CustomUser, Connection


User= get_user_model()


# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets, 'user': request.user})

@csrf_exempt
@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete() 
        liked = False
    else:
        liked = True 

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
            tweet = form.save(commit=False)
            tweet.user = request.user
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



def user_search(request):
    query = request.GET.get('query', '').strip()
    results = []
    
    if query:
        users = User.objects.filter(username__icontains=query)[:5]  # Limit the number of results
        results = [{"username": user.username,"user_id" : user.id,"profile_image": user.user_profile_image.url if user.user_profile_image else "/static/default_profile.png"} for user in users]
        
    return JsonResponse({"results": results})


@login_required
def user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    followers_count = Connection.objects.filter(receiver=user, status=True).count()
    following_count = Connection.objects.filter(sender=user, status=True).count()
    is_following = Connection.objects.filter(sender=request.user, receiver=user, status=True).exists()
    is_self = user == request.user

    context = {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'is_self': is_self,
    }

    return render(request, 'user_details.html', context)

@login_required
def follow(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user != request.user:
        connection, created = Connection.objects.get_or_create(sender=request.user, receiver=target_user)

        if connection.status:
            connection.unfollow()
        else:
            connection.follow()

    return redirect('user_details', user_id=user_id)


