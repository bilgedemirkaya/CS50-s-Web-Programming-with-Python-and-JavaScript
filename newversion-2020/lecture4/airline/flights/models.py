from django.db import models

# Create your models here.
"""
Here we are going to define what models are going to exist for our application. Every model is going to be python class
You can think of one model as a table 

"""
"""
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
"""

"""
We create a table but yet we dont have a database.
We should now tell Django that you should update database to include info about the models we have created.
This is a process that we refer to in Django as ~ Migrations
** to make the migrations type in command: 
python manage.py makemigrations
"""

"""
It created the database db.sqlite3 you can see in flights folder (also check in the migration directory.) 
Now type in command to apply this migration: 
python manage.py migrate
"""

"""
In order to interact with database I could just use sql syntax by opening up sqlite3 but Django provides some 
abstraction layers so no need to execute those commands myself. So I can enter Djangos's shell 
where I can run Python commands by running:
python manage.py shell. In this shell you can speak to database
"""

"""
First thing you do is typing:
from flights.models import Flight
(flights is name of a app, models is name name of a file, Flight is the name of class)
now we can create a new flight for example: 
f = Flight(orif gin="New York", destination= "London", duration="415")
f.save()

so this is the python way of inserting data into the database
"""

"""
Flight.objects.all() is the equivalent of saying SELECT * FROM flights
but output is only <QuerySet [<Flight: Flight object (1)>]>
so it would be nicer to see clean data from this table. Thats why we applied def __str__ function.
Now we can see output is cleaner <QuerySet [<Flight: 1: New York to London>]>
examples:
flight = Flight.objects.all()
>>> flight = flight.first()
>>> flight
>>> flight.origin 
>>> flight.delete()
exc
"""

"""
Now lets create another table, and look at relationships
"""

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)


    def __str__(self):
        return f"{self.city} ({self.code})"

"""
Now our flight model needs to change. No longer will origin and destination be character fields that just storing text,
but instead its going to be like this
"""
class Flight(models.Model):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departures")
    # foreign key references to another table. When I have tables that related to each other SQL need to know
    # what should happen if you delete something on_delete_models.CASCADE means if I ever delete airport, its also
    # going to delete any of the corresponding flight. or you can put models.protect to dont let you delete the airport
    # if you have a related data.related_name is a way of accessing a relationship in the reverse order:
    # if I have the airport code how do I access origin value that all flight from that airport.
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

"""
So this is changed in python code but not in the database itself. In order to apply those changes do the 2 step migration process 
again
Now in the shell you can create a new airport like:
>>> jfk = Airport(code="JFK",city = "New York")
>>> jfk.save()
>>> lhr = Airport(code="LHR", city = "London")
>>> lhr.save()
>>> cdg = Airport(code="CDG", city = "Paris")
>>> cdg.save()
>>> nrt = Airport(code="NRT", city = "Tokyo")
>>> nrt.save()
>>> f = Flight(origin=jfk,destination=lhr,duration=415)
>>> f.save()
(Notice that we use airport codes for origin and destination)
Now I can run a command like:
>>> f.origin.city
'New York'
>>> lhr.arrivals.all() will give all the flight that have lhr origins.
"""

"""
Now lets create passenger class. It needs to have many to many relationship with flights:
Every passenger has a flight associate with them,but any passenger could be associate with may flights. So we use 
ManyToManyField
"""
class Passengers(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight,blank=True,related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"

# now apply these changes as
# add this class to the admin.py