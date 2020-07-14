from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import operator



from .models import User,Listings,Comments,Bid
from .forms import CommentForm,BidForm


def index(request):

# '-' to do it in descending order
    return render(request, "auctions/index.html",{"listings":Listings.objects.filter(status="ACTIVE").order_by('-listing_date')})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def pagedetails(request,title):
    listing = Listings.objects.filter(title=title).first()
    if listing.status == "CLOSED":
        return HttpResponseRedirect ("/closelisting/"+title)
    bids = Bid.objects.filter(list=listing).order_by('-bid_date')
    bidslist = []
    currentuser= request.user
    for p in bids:
        bid = p.bid
        bidslist.append(bid)
    if bidslist != []:
        currentprice = max(bidslist)
    else:
        currentprice = listing.startingbid
    if currentuser == listing.owner:
        messages.add_message(request, messages.SUCCESS, "If you close your listing, it will be sold to whom made the best offer")
        return render(request, "auctions/listownerspage.html",
                      {"listing": listing, "form": CommentForm,
                       "comments": Comments.objects.filter(list=listing), "bids": bids,
                       "bidform": BidForm, "currentprice": currentprice
                       })


    return render(request, "auctions/pagedetails.html",
                      {"listing": listing, "form": CommentForm,
                       "comments": Comments.objects.filter(list=listing), "bids": bids,
                       "bidform": BidForm, "currentprice": currentprice
                       })
@login_required(login_url='/login')
def newlisting(request):
    currentuser = request.user
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        startingbid = request.POST['startingbid']
        url = request.POST['url']
        if url is None:
            myfile = request.FILES['image',False]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
    
            Listings.objects.create(title=title,description=description,startingbid=startingbid,category=category,image=filename,owner=currentuser)
        else:
            Listings.objects.create(title=title,description=description,startingbid=startingbid,category=category,url=url,owner=currentuser)

        messages.add_message(request,messages.SUCCESS,'Your listing is created succesfully')

        return HttpResponseRedirect('/')
    else:
        return render(request,"auctions/newlisting.html")
@login_required(login_url='/login')
def watchlist(request):
   if "watch" not in request.session:
       request.session["watch"] = []
       return render(request, 'auctions/watchlist.html', {"watchlists": request.session["watch"]})
   else:
       watchlist = request.session["watch"]
       return render(request, 'auctions/watchlist.html', {"watchlists": watchlist})


@login_required(login_url='/login')
def add(request,title):

    watchlists = Listings.objects.filter(title=title).first()
    if "watch" not in request.session:
        request.session["watch"] = []
    if watchlists.title in request.session["watch"]:
        messages.add_message(request, messages.SUCCESS, "This item is in already in the watchlist")
        return HttpResponseRedirect('/watchlist')
    request.session["watch"] += [watchlists.title]
    request.session.modified = True
    messages.add_message(request, messages.SUCCESS,"Successfully added")
    return render(request, 'auctions/watchlist.html', {"watchlists": request.session["watch"]})


@login_required(login_url='/login')
def remove(request,title):
    """The django session object can only save when its modified. But because you are
     modifying an object within session, the session object doesn't know its being modified and hence it cant save."""
    watchlists = Listings.objects.filter(title=title).first()
    try:
        request.session['watch'].remove(watchlists.title)
    except:
        messages.add_message(request, messages.WARNING, "This item was not in the watchlist")
        return HttpResponseRedirect('/watchlist')
    messages.add_message(request,messages.SUCCESS,"Successfully removed")
    request.session.modified = True

    return render(request, 'auctions/watchlist.html', {"watchlists": request.session["watch"]})

def category(request):
    lists = Listings.objects.all()
    categories = []
    for list in lists:
        category = list.category
        if category not in categories:
            categories.append(category)
    return render(request,'auctions/category.html',{"categories":categories})

def categorysort(request, category):
    lists = Listings.objects.filter(category=category)
    return render(request, "auctions/index.html", {"listings": lists})

@login_required(login_url='/login')
def comment(request,title):
    if request.method == "POST":
       form = CommentForm(request.POST)
       user = request.user
       listing = Listings.objects.filter(title=title).first()
       if form.is_valid():
           comment = form.cleaned_data['comment']
           Comments.objects.create(user=user, list=listing, comment=comment)
           return HttpResponseRedirect('/'+ title)

    else:
        return HttpResponseRedirect('/')
@login_required(login_url='/login')
def bidding(request,title):
    if request.method == "POST":
        listing = Listings.objects.filter(title=title).first()
        bids = Bid.objects.filter(list=listing)
        bidslist = []
        userlist = []
        for p in bids:
            bid = p.bid
            bidslist.append(bid)
            u = p.user
            userlist.append(u)
        if bidslist != []:
            currentprice = max(bidslist)
        else:
            currentprice = listing.startingbid
        form = BidForm(request.POST)
        user = request.user


        if form.is_valid():
           last_bid = form.cleaned_data['bid']
           print(last_bid)
           if currentprice >= last_bid:
               messages.add_message(request,messages.WARNING,"Your bid must be greater than current price")
               return HttpResponseRedirect('/' + title)
           else:
               Bid.objects.create(user=user, list=listing, bid=last_bid)
               messages.add_message(request, messages.WARNING, "Succesfully made bid on item")
               return HttpResponseRedirect('/' + title)
        else:
           messages.add_message(request, messages.WARNING, "Invalid form")
           return render(request, "auctions/pagedetails.html",
                         {"listing": listing, "form": CommentForm,
                          "comments": Comments.objects.filter(list=listing), "bids": bids,
                          "bidform": BidForm, "currentprice": currentprice
                          })
    else:
        return HttpResponseRedirect('/')
def closed(request):
    return render(request, "auctions/closedlistings.html",
                  {"listings": Listings.objects.filter(status="CLOSED").order_by('listing_date')})


def closelisting(request,title):
    listing = Listings.objects.filter(title=title).first()
    bids = Bid.objects.filter(list=listing).order_by('-bid_date')
    bidslist = {}
    currentuser = request.user
    for p in bids:
        bid = p.bid
        bidowner = p.user
        bidslist.update({bidowner: bid})

    if bidslist != {}:
        currentprice = max(bidslist.values())
        winner = max(bidslist.items(), key=operator.itemgetter(1))[0]
    else:
        currentprice = listing.startingbid
        winner = "Nobody"
    listing.status = "CLOSED"
    listing.save()

    if currentuser == winner:
        messages.add_message(request, messages.SUCCESS,
                             "Congrats, you won the auction!")
    if not messages:
        messages.add_message(request, messages.SUCCESS,
                         "Succesfully closed listing")

    return render(request, "auctions/sold.html",
                  {"listing": listing, "form": CommentForm,
                   "comments": Comments.objects.filter(list=listing), "bids": bids,
                   "currentprice": currentprice,"winner":winner
                   })