from django.shortcuts import render
import datetime

def index(request):
    now = datetime.datetime.now()
    # if now.day is 1 and now.month is one, value of my newyear variable is going to be true
    return render(request, "newyear/newyear.html",{"newyear":now.day == 1 and now.month == 1})