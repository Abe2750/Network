# from asyncio.windows_events import NULL
import json
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.core.paginator import Paginator


from .models import Post, User



def index(request):
    if request.method == "POST":
        Postform = PostForm(request.POST)
    else:
        post_list = Post.objects.order_by("-timeStamp").all()
        paginator = Paginator(post_list, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/index.html', 
        {
        "posts" : Post.objects.order_by("-timeStamp").all(),
        'page_obj': page_obj,
        
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

@login_required
@csrf_exempt
def post(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method should be POST."}, status=404)
    # Create Post
    else:
        data = json.loads(request.body)
    
        post = Post.objects.create(postNote = data.get("posttext"), poster = request.user)
        post.save()
        return JsonResponse({"message": "Post Successful."}, status=201)
     
def profile(request, profile):
    profile = User.objects.get(username = profile)
    print(request.user.is_authenticated and request.user == profile)
    if request.user.is_authenticated:
        text = "unfollow" if profile.followers.contains(request.user) else "follow"
    else : 
        text ="ignore" #shouldn't be displayed

    post_list = Post.objects.order_by("-timeStamp").filter(poster = profile)
    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/profilePage.html', 
        {'profile': profile,
         "page_obj" : page_obj, 
         'isSelf' : (request.user.is_authenticated and request.user == profile ),
         'follow' : text,
         'followers' : profile.count_followers(),
         'following' : profile.count_following(),

          })

@csrf_exempt
def follow(request, profile):
    profile = User.objects.get(username = profile)
    if request.user == profile :
        pass
    elif profile.followers.contains(request.user):
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    post_list = Post.objects.order_by("-timeStamp").all()
    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', 
        {
        "page_obj" : page_obj, 
            })
def following(request):
    follows = User.objects.filter(followers=request.user)
    post_list = Post.objects.order_by("-timeStamp").filter(poster__in= follows)
    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', 
        {
        "page_obj" : page_obj, 
            })
@login_required
@csrf_exempt
def edit(request):
    print("we here baby")
    if request.method != "POST":
        return JsonResponse({"error": "Method should be POST."}, status=404)
    # Edit Post
    else:
        
        data = json.loads(request.body)
        id = data.get("post_id")
        post = Post.objects.get(post_id = id)
       
        post.postNote = data.get("posttext")

        post.save()

        return JsonResponse({"message": "Post Successful.", "id" : id,"postNote" : post.postNote }, status=201)

@login_required
@csrf_exempt
def like(request):
    if request.method != "POST":
        return JsonResponse({"error" : "Method should be POST."}, status = 404)
    else:
        data = json.loads(request.body)
        id  = data.get("post_id")
        post = Post.objects.get(post_id = id)
        if request.user == post.poster :
            print("hello1")
            return JsonResponse({"message": "Post Successful.", "id" : id,
            "nlikes" : post.likes, 
            'check' :  post.likers.all().contains(request.user),
            }, status=201)
        if request.user in post.likers.all():
            print("hello2")
            post.likes -=1
            post.likers.remove(request.user)
        else:
            print("hello3")
            post.likes +=1
            post.likers.add(request.user)
        post.save()
        print(request.user in post.likers.all())
        return JsonResponse({"message": "Post Successful.", "id":id,"nlikes":post.likes,
                'check' :  post.likers.all().contains(request.user),
        }, status=201)