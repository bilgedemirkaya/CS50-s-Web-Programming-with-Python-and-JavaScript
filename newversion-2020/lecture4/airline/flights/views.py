from django.shortcuts import render
from .models import Flight,Passengers
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):

    #it will give access to all of the flights that I have in the database currently
    return render(request,"flights/index.html",{
        "flights": Flight.objects.all()
    })
def flight(request,flight_id):
    # pk is primary key which refering to the id
    flight = Flight.objects.get(pk=flight_id)
    # we can do flight.passengers.all() bcs passengers is our related name
    # flight is our flight object that we got from Flight table
    return render(request,"flights/flight.html",{"flight":flight,"passengers":flight.passengers.all(),
                                                 "nonpassengers":Passengers.objects.exclude(flights=flight).all()})
def book(request,flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passengers.objects.get(pk=int(request.POST["passenger"]))
        # access to passenger`s flights and add this particular flight in it
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight",args=(flight.id,)))