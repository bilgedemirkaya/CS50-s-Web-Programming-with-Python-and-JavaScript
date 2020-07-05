from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newentry", views.newentry, name="newentry"),
    path("randomed", views.randomed, name="randomed"),
    path("<str:title>", views.title, name="title"),
    path("<str:title>/edit", views.edit, name="edit"),
]