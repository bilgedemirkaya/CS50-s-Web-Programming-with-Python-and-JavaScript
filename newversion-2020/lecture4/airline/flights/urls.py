from django.urls import path

from . import views

"""
   before dealing with actual urls, first create some models. Models are going to be a way of creating class
   that is going to represent data tht I want Django to store inside of a database.  
"""

urlpatterns=[
path("",views.index,name="index"),
path("<int:flight_id>",views.flight, name="flight"),
path("<int:flight_id>/book",views.book, name='book')
]
