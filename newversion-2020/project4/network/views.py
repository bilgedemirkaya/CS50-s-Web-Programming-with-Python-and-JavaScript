from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import UserProfile,User


def index(request):
    try:
        user = request.user
        name = UserProfile.objects.filter(user = user).first()
        allposts = UserPosts.objects.all()
        return render(request, "network/index.html",{"name" : name.firstname,"allposts":allposts})
    except:
         return render(request, "network/login.html")

def profile(request):
    user = request.user
    profile = UserProfile.objects.filter(user = user).first()
    userposts = UserPosts.objects.filter(owner = user.profile).all()
    return render(request,"network/profile.html",{"userposts" : userposts,"name" : profile.firstname,"profile":profile})

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
        firstname = request.POST["firstname"]
        city = request.POST["city"]

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
        UserProfile.objects.create(user = user, city=city,firstname=firstname) 
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
