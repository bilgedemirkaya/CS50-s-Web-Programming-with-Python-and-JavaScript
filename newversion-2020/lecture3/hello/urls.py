from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bilge", views.bilge, name="genius"),
    path("<str:isim>",views.vari,name="whatever")
]