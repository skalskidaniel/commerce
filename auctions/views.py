from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True)
    
    return render(request, "auctions/index.html", {
        'listings' : listings
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

@login_required
def create_listing(request):
    if request.method == "POST":
        author = request.user
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        image = request.POST.get('image', None)
        category = request.POST['category']
        
        listing = Listing(author=author,
                          title=title,
                          description=description, 
                          starting_bid=starting_bid, 
                          image=image, 
                          category=category
                        )
        listing.save()
        
        return HttpResponseRedirect(reverse("my_listings"))
    else:
        context = {
        'Listing': Listing,
        }
        return render(request, 'auctions/create_listing.html', context)
    
def view_listing(request, listing_id, error_message=None):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by('-addition_time')
    in_watchlist = request.user.is_authenticated and listing in request.user.watchlist.all()

    return render(request, 'auctions/view_listing.html', {
        'listing_id': listing.id,
        'title': listing.title,
        'category': Listing.CATEGORIES[listing.category],
        'author': listing.author,
        'time': listing.addition_time,
        'image': listing.image,
        'bid': listing.current_bid,
        'description': listing.description,
        'in_watchlist': in_watchlist,
        'active': listing.is_active,
        'winner': listing.winner,
        'comments': comments,
        'error_message': error_message  # Pass the error message to the template
    })
    
    
def show_categories(request):
    categories = Listing.CATEGORIES
    
    return render(request, 'auctions/categories_all.html', {
        'categories' : categories
    })
        
def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, is_active=True)
    
    return render(request, 'auctions/category_listings.html', {
        'category_name' : Listing.CATEGORIES.get(category_name),
        'listings' : listings
    })
    
@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        'watchlist' : watchlist
    })
    
@login_required
def watchlist_toggle(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user

    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)

    return redirect('view_listing', listing_id=listing_id)

@login_required
def place_bid(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        author = request.user
        value = int(request.POST['bid_value'])

        bid = Bid(author=author,
                  listing=listing,
                  value=value)
        try:
            bid.save()
        except ValidationError as err:
            return view_listing(request, listing_id, error_message=str(err.messages[0]))

        return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))
    
@login_required
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.is_active = False
        if listing.current_bid != 0:
            highest_bid = Bid.objects.get(listing=listing, value=listing.current_bid)
            listing.winner = highest_bid.author
        listing.save()
        
        return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))
    
@login_required
def add_comment(request, listing_id):
    author = request.user
    listing = Listing.objects.get(id=listing_id)
    content = request.POST['content']
    comment = Comment(author=author,
                      listing=listing,
                      content=content
                      )
    comment.save()
    
    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))

@login_required
def user_listings(request):
    listings = Listing.objects.filter(author=request.user)
    
    return render(request, 'auctions/user_listings.html', {
        'listings' : listings
    })