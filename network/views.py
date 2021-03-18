import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Post, User

# Sending information for pagination to index
def index(request):
    posts = Post.objects.all().order_by('-post_time')
    likes = []
    user_like = []
    for post in posts:
        likes.append(post.post_likes.all().count())
        user_like.append(request.user in post.post_likes.all())
    
    #Creating an object paginator with a data structure with all information needed
    paginator = Paginator(tuple(zip(posts, likes, user_like)), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # User posts
    if request.user.is_authenticated:
        user_posts = request.user.posts.all()
    else:
        user_posts = []
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "user_posts": user_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Create a new post
@login_required(login_url="login")
def new_post(request):
    if request.method == "POST":
        content = request.POST["post_content"]
        p = Post(post_user = request.user, post_content = content)
        p.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")


#Update an specific post to increase o decrease its likes
@csrf_exempt
@login_required(login_url="login")
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data.get("id"))
        user = request.user
        if user in post.post_likes.all():
            user.user_likes.remove(post)
        else:
            user.user_likes.add(post)
        user.save()
        return JsonResponse({
            "user_like": user in post.post_likes.all(),
            "likes": post.post_likes.all().count()
        })
    return JsonResponse({
            "error": "PUT request required."
        }, status=400)


def profile(request, username):
    # Get user information
    user_profile = User.objects.get(username=username)
    following = user_profile.user_following.all().count()
    followers = user_profile.user_followers.all().count()

    # See if user follow this user_profile
    user_follow = request.user in user_profile.user_followers.all()

    # Get all posts with likes and users that have liked
    posts = Post.objects.filter(post_user=user_profile).order_by('-post_time')
    likes = []
    user_like = []
    for post in posts:
        likes.append(post.post_likes.all().count())
        user_like.append(request.user in post.post_likes.all())
    
    #Creating an object paginator with a data structure with all information needed
    paginator = Paginator(tuple(zip(posts, likes, user_like)), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # User posts
    if request.user.is_authenticated:
        user_posts = request.user.posts.all()
    else:
        user_posts = []
    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "user_profile": user_profile,
        "following": following,
        "followers": followers,
        "user_follow": user_follow,
        "user_posts": user_posts
    })


# Function to follow and unfollow
@csrf_exempt
@login_required(login_url="login")
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_profile = User.objects.get(id=data.get("id"))
        user = request.user
        if not user == user_profile:
            if user in user_profile.user_followers.all():
                user.user_following.remove(user_profile)
            else:
                user.user_following.add(user_profile)
            user.save()
        return JsonResponse({
            "user_follow": user in user_profile.user_followers.all(),
            "following": user_profile.user_following.all().count(),
            "followers": user_profile.user_followers.all().count()
        })
    return JsonResponse({
            "error": "POST request required."
        }, status=400)


# Get only posts from users some user follows
@login_required(login_url="login")
def following(request):
    all_posts = Post.objects.all().order_by('-post_time')
    posts = []
    for p in all_posts:
        if p.post_user in request.user.user_following.all():
            posts.append(p)
    likes = []
    user_like = []
    for post in posts:
        likes.append(post.post_likes.all().count())
        user_like.append(request.user in post.post_likes.all())
    
    #Creating an object paginator with a data structure with all information needed
    paginator = Paginator(tuple(zip(posts, likes, user_like)), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@csrf_exempt
@login_required(login_url="login")
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data.get('id'))
        if post in request.user.posts.all():
            new_content = data.get('content')
            post.post_content = new_content
            post.post_time = datetime.datetime.now()
            post.save()
            return JsonResponse({
                "new_content": post.post_content,
                "new_time": post.post_time.strftime("%B %d, %Y, %I:%M %p")
            })
        else:
            return JsonResponse({
                "error": "You are not the user who post this.",
                "new_content": post.post_content,
                "new_time": post.post_time.strftime("%B %d, %Y, %I:%M %p")
            }, status=203)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)