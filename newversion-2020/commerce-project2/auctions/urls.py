from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed",views.closed, name="closed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories",views.category,name="categories"),
    path("comment/<str:title>",views.comment,name ="comment"),
    path("categorysort/<str:category>", views.categorysort, name="categorysort"),
    path("<str:title>", views.pagedetails, name="pagedetails"),
    path("watchlistadd/<str:title>",views.add, name="add"),
    path("watchlistremove/<str:title>",views.remove, name="remove"),
    path("bidding/<str:title>",views.bidding, name="bidding"),
    path("closelisting/<str:title>",views.closelisting, name="closelisting")
]