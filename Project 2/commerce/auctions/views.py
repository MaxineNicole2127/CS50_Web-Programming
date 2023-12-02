from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment

categories = []
listers = []

def index(request):
    return render(request, "auctions/index.html", {
        "title" : "Active Listings",
        "listings" : Listing.objects.filter(is_active = True).all()
    })


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

@login_required(login_url="/login")
def create(request):
    if(request.method == "POST"):
        title = request.POST["title"]
        description = request.POST["description"]
        category_name = request.POST["category"]
        if(not Category.objects.filter(category_title = category_name).exists()):
            newCategory = Category(category_title = category_name)
            newCategory.save()
        category = Category.objects.get(category_title = category_name)
        img_url = request.POST["img_url"]
        starting_bid = request.POST["starting_bid"]
        lister_pk = request.POST["lister"]
        lister = User.objects.get(pk = lister_pk)
        newListing = Listing(listing_title = title, lister = lister, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
        newListing.save()
        
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createListings.html", {
        "category_list" : Category.objects.exclude(category_title = "None").all()
    })

# @login_required(login_url="/login")
# def create(request):
#     if(request.method == "POST"):
#         title = request.POST["title"]
#         description = request.POST["description"]
#         category_name = request.POST["category"]

#         '''if(category_name == "None" or category_name == "" or category_name == "none"):
#             category = Category.objects.get(category_title = "None")
#         elif(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()'''
#         '''
#         if(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()'''
        
#         if(category_name == "None" or category_name == "" or category_name == "none"):
#             category = Category.objects.get(category_title = "None")
#         elif(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()
#             category = Category.objects.get(category_title = category_name)
#         img_url = request.POST["img_url"]
#         starting_bid = request.POST["starting_bid"]
#         lister_pk = request.POST["lister"]
#         lister = User.objects.get(pk = lister_pk)
#         newListing = Listing(listing_title = title, lister = lister, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#         newListing.save()
        
#         return HttpResponseRedirect(reverse("index"))

#     return render(request, "auctions/createListings.html", {
#         "category_list" : Category.objects.exclude(category_title = "None").all()
#     })
#     '''
#     if(request.method == "POST"):
#         form = ListingForm(request.POST)
#         if(form.is_valid()):
#             title = form.cleaned_data["title"]
#             description = form.cleaned_data["description"]
#             category_pk = int(form.cleaned_data["category"])
#             category = Category.objects.get(pk = category_pk)
#             starting_bid = form.cleaned_data["price"]
#             img_url = form.cleaned_data["img_url"]

#             form.cleaned_data["lister"] = request.POST["lister"]
#             lister_pk = int(form.cleaned_data["lister"])
#             lister = User.objects.get(pk = lister_pk)

#             # newListing = Listing(listing_title = title, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#             newListing = Listing(listing_title = title, lister = lister, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#             newListing.save()
#             # Listing.objects.create()
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "auctions/createListings.html", {
#                 "form": ListingForm(),
#                 "message" : "Failed!"
#             })

#     return render(request, "auctions/createListings.html", {
#         "form": ListingForm()
#     })
#     '''
########################
# def create(request):
#     if(request.method == "POST"):
#         title = request.POST["title"]
#         description = request.POST["description"]
#         category_name = request.POST["category"]

#         '''if(category_name == "None" or category_name == "" or category_name == "none"):
#             category = Category.objects.get(category_title = "None")
#         elif(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()'''
#         '''
#         if(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()'''
        
#         if(category_name == "None" or category_name == "" or category_name == "none"):
#             category = Category.objects.get(category_title = "None")
#         elif(not Category.objects.filter(category_title = category_name).exists()):
#             newCategory = Category(category_title = category_name)
#             newCategory.save()
#             category = Category.objects.get(category_title = category_name)
#         img_url = request.POST["img_url"]
#         starting_bid = request.POST["starting_bid"]
#         lister_pk = request.POST["lister"]
#         lister = User.objects.get(pk = lister_pk)
#         newListing = Listing(listing_title = title, lister = lister, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#         newListing.save()
        
#         return HttpResponseRedirect(reverse("index"))

#     return render(request, "auctions/createListings.html", {
#         "category_list" : Category.objects.exclude(category_title = "None").all()
#     })
#     '''
#     if(request.method == "POST"):
#         form = ListingForm(request.POST)
#         if(form.is_valid()):
#             title = form.cleaned_data["title"]
#             description = form.cleaned_data["description"]
#             category_pk = int(form.cleaned_data["category"])
#             category = Category.objects.get(pk = category_pk)
#             starting_bid = form.cleaned_data["price"]
#             img_url = form.cleaned_data["img_url"]

#             form.cleaned_data["lister"] = request.POST["lister"]
#             lister_pk = int(form.cleaned_data["lister"])
#             lister = User.objects.get(pk = lister_pk)

#             # newListing = Listing(listing_title = title, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#             newListing = Listing(listing_title = title, lister = lister, listing_description = description, listing_category = category, img_url = img_url, starting_bid = starting_bid)
#             newListing.save()
#             # Listing.objects.create()
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "auctions/createListings.html", {
#                 "form": ListingForm(),
#                 "message" : "Failed!"
#             })

#     return render(request, "auctions/createListings.html", {
#         "form": ListingForm()
#     })
#     '''

def listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "no_of_bids" : len(listing.biddings.all()),
        "comments" : listing.comments.all(),
        "biddings" : listing.biddings.all(),
        "listing_watchers" : listing.watchers.all(),
        "no_of_comments" : len(listing.comments.all())
    })

@login_required(login_url="/login")
def endAuction(request, listing_id):
    if(request.method == "POST"):
        # listing_to_end = int(request.POST["listing_id"])
        listing_to_end = listing_id
        listing = Listing.objects.get(pk = listing_to_end)
        listing.is_active = False

        listing.save()

        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="/login")
def deleteListing(request, listing_id):
    if(request.method == "POST"):
        # listing_to_end = int(request.POST["listing_id"])
        listing_to_end = listing_id
        listing = Listing.objects.get(pk = listing_to_end)
        listing.delete()

        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="/login")
def addToWatchlist(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = User.objects.get(username = request.POST["username"])
    user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("watchlist", args = (user.id,)))

@login_required(login_url="/login")
def watchlist(request, user_id):
    watcher = User.objects.get(pk = user_id)
    # return render(request, "auctions/watchlist.html", {
    #     "watchlist" : watcher.watchlist.all()
    # })
    return render(request, "auctions/index.html", {
        "page_type" : "watchlist",
        "title" : watcher.username + "'s Watchlist",
        "listings" : watcher.watchlist.exclude(is_active = False).all()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.exclude(category_title = "None").all()
        #Passenger.objects.exclude(flights = flight).all()
    })

def category(request, category_id):
    category = Category.objects.get(id = category_id)
    return render(request, "auctions/index.html", {
        "page_type" : "category",
        "title" : category.category_title,
        "listings" : category.categorizing.exclude(is_active = False).all()
    })

@login_required(login_url="/login")
def bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if(request.method == "POST"):
        bid_price = request.POST["bid"]
        bidder = User.objects.get(pk = int(request.POST["bidder"]))
        
        if(listing.biddings.filter(bid_price = bid_price).exists()):
            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "no_of_bids" : len(listing.biddings.all()),
                "comments" : listing.comments.all(),
                "biddings" : listing.biddings.all(),
                "message" : "Please input an amount higher than the highest bid."
            })

        else:
            bidding = Bid(bid_price = bid_price, bidder = bidder, listing = listing)
            bidding.save()
            listing.highest_bid = bidding.bid_price
            listing.buyer = bidding.bidder
            listing.save()

            return HttpResponseRedirect(reverse("listing", args = (listing_id,)))

        

'''
@login_required(login_url="/login")
def bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if(request.method == "POST"):
        bid_price = request.POST["bid"]
        bidder = User.objects.get(pk = int(request.POST["bidder"]))
        bidding = Bid(bid_price = bid_price, bidder = bidder, listing = listing)
        bidding.save()

        listing.highest_bid = bidding.bid_price
        listing.buyer = bidding.bidder
        listing.save()

        #return HttpResponseRedirect(reverse("listing", args = (listing_id,)))
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "no_of_bids" : len(listing.biddings.all()),
            "comments" : listing.comments.all(),
            "to_compare_to" : float(listing.highest_bid) + 1,
            "biddings" : listing.biddings.all()
        })


@login_required(login_url="/login")
def bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if(request.method == "POST"):
        bid_price = request.POST["bid"]
        bidder = User.objects.get(pk = int(request.POST["bidder"]))
        bidding = Bid(bid_price = bid_price, bidder = bidder, listing = listing)
        bidding.save()

        listing.highest_bid = bidding.bid_price
        listing.buyer = bidding.bidder
        listing.save()

        #return HttpResponseRedirect(reverse("listing", args = (listing_id,)))
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "no_of_bids" : len(listing.biddings.all()),
            "comments" : listing.comments.all(),
            "to_compare_to" : float(listing.highest_bid) + 1,
            "biddings" : listing.biddings.all()
        })

'''


@login_required(login_url="/login")
def addComment(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if(request.method == "POST"):
        comment_content = request.POST["comment"]
        commenter = User.objects.get(pk = int(request.POST["commenter"]))
        comment = Comment(content = comment_content, commenter = commenter, listing = listing)
        comment.save()

        # listing.comments.add(comment)

        return HttpResponseRedirect(reverse("listing", args = (listing_id,)))
    

def deleteFromWatchlist(request, user_id):
    user = User.objects.get(pk = user_id)
    if(request.method == "POST"):
        listing = Listing.objects.get(pk = int(request.POST["listing"]))
        user.watchlist.remove(listing)

        return HttpResponseRedirect(reverse("watchlist", args = (user.id,)))
    
def closedListings(request): #for the list
    return render(request, "auctions/index.html", {
        "page_type" : "closed listings",
        "title" : "Closed Listings",
        "listings" : Listing.objects.filter(is_active = False).all()
    })


def closedListing(request, listing_id): #for the product details
    listing = Listing.objects.get(id = listing_id)
    return render(request, "auctions/closedListing.html", {
        "listing" : listing,
        "no_of_comments" : len(listing.comments.all()),
        "comments" : listing.comments.all(),
        "biddings" : listing.biddings.all()
    })