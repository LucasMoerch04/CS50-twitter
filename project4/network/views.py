import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import *
import datetime, timeago
from django.utils import timezone

# Translates the time and date message based on original posttime
def get_time(posts):
    now = timezone.now()
    for post in posts:
        if post.datetime > now-datetime.timedelta(seconds=86400):
            msg = timeago.format(post.datetime, now, 'en_short')
            post.datetime = msg.replace('ago', '')
        else:
            post.datetime = post.datetime.strftime("%b %d")


def index(request):
    posts = Post.objects.all().order_by('-datetime')
    get_time(posts)
    posts = paginate(request, posts)
    user = request.user
    
    user_likes = Like.objects.filter(user=request.user.id)
    user_liked_posts = [like.post.id for like in user_likes]
    
    
    return render(request, "network/index.html", {
        "posts": posts,
        "user": user,
        "user_liked_posts": user_liked_posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        try: 
            username = request.POST["username"]
        except:
            return render(request, "network/login.html")
        
        
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
            f = Follow.objects.create(profile=user.id)
            f.save()

            
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def new_post_view(request):
    if request.method == "POST":
        author = request.user
        body = request.POST["body"]
        time =  timezone.localtime()
        image = request.POST["dataURL"]
        print(image)
        
        if image:
            post = Post(author=author, body=body, datetime=time, image=image)
            post.save()
        else:        
            post = Post(author=author, body=body, datetime=time)
            post.save()
        
        return HttpResponseRedirect(reverse("index"))

def profile_page_view(request, profile_id):
    user = request.user
    profile = User.objects.get(id=profile_id)
    posts = Post.objects.filter(author=profile_id).order_by('-datetime')
    get_time(posts)
    #Following count
    f = Follow.objects.get(profile=profile_id)
    following_count = len(f.following_list.all())
    
    #Followers count
    fs = Follow.objects.get(profile=profile_id)
    followers_count = len(fs.follower_list.all())
    

    if user in fs.follower_list.all():
        followBtn = "Unfollow"
    else:
        followBtn = "Follow"

    posts = paginate(request, posts)
    
    return render(request, "network/profile.html",{
        "profile": profile,
        "posts": posts,
        "following_count": following_count,
        "follower_count": followers_count,
        "followBtn": followBtn
    })
    
def follow(request, profile_id):
    if request.method == "POST":
        user = request.user
        profile = User.objects.get(id=profile_id)
        
        f = Follow.objects.get(profile=user.id)
    

        u = Follow.objects.get(profile=profile_id)

        #If target is in following list
        if profile in f.following_list.all():
            #Unfollow
            f.following_list.remove(profile)
            #Remove from followers list
            u.follower_list.remove(user)

            
        #Else
        else: 
            #Add to users following
            f.following_list.add(profile)
            #Add to targets followers list
            u.follower_list.add(user)

        return HttpResponseRedirect(reverse("profile", args=(profile_id,)))
        
def following_view(request):
    user = request.user
    following = Follow.objects.get(profile=user.id)
    following = following.following_list.all()
    posts = Post.objects.filter(author__in=following).order_by('-datetime')

    return render(request, "network/index.html", {
        "posts": posts
    })

def paginate(request, objects):
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    print(page_number)
    try:
        page_obj = paginator.page(request.GET.get("page"))
    except:
        page_obj = paginator.page(1)
    return page_obj
    
@csrf_exempt
@login_required    
def edit_post(request):
    data = json.loads(request.body)
    body = data.get("body", "")
    post_id = data.get("id", "")

    

    # Fetch the post to be edited
    post = Post.objects.get(id=post_id)
    if post.author == request.user:
        post.body = body
        post.save()
    else:
        print("no allow")
        
        
    return JsonResponse({"message": "Changes saved"}, status=201)

@csrf_exempt
@login_required    
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get("post", "")
    user = request.user
    
    post = Post.objects.get(id = post_id)
    
    try: 
        post_like = Like.objects.get(post = post, user=user)
        post_like.delete()
        print("delete")
        return JsonResponse({"message": "Disliked"}, status=201)
    except:
        post_like = Like(post = post, user = user)
        post_like.save()
        print("like")
        return JsonResponse({"message": "Liked"}, status=201)


@csrf_exempt
@login_required        
def changePfp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        imgSrc = data.get("imgSrc", "")
        user = request.user
        
        try:
            user = User.objects.get(username = user)
            
            user.pfp = imgSrc
            user.save()
            print("workde")
            return JsonResponse({"message": "Profile Picture ChangeD"}, status=201)
        
        except:
            return JsonResponse({"message": "Profile Picture Change Did Not Work"}, status=201)



    


        
        
