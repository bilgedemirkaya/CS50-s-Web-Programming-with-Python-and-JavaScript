from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'hello/index.html')
def bilge(request):
    return HttpResponse("hello genius")
def greet(request,name):
    return HttpResponse(f"hello genius {name}!")
def vari(request,isim):
    return render(request,'hello/isim.html',{"isim":isim.capitalize()})