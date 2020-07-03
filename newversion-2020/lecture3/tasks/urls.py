from django.urls import path
from . import views

urlpatterns= [
    path("", views.index, name="tasks"),
    path("add/", views.add, name="add")
]
