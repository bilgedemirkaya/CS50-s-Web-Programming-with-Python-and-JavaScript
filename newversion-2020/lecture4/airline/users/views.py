from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

"""

request object that passed in as part of the request to every user in Django automatically has a user attribute 
associated with it. User object has an authenticated attribute that tells if the user authenticated or not

"""
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request,"users/user.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username,password= password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"users/login.html",{
                "message":"Invalid credentials"
            })
    return render(request, "users/login.html")
def logout_view(request):
    logout(request)
    return render(request,"users/login.html",{
        "message":"User has been logged out."
    })