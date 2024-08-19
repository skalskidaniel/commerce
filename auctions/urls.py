from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name='create_listing'),
    path("view/<int:listing_id>", views.view_listing, name="view_listing"),
    path("categories", views.show_categories, name="show_categories"),
    path("category/<str:category_name>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/toggle/<int:listing_id>", views.watchlist_toggle, name='watchlist_toggle'),
    path("bid/place/<int:listing_id>", views.place_bid, name='place_bid')
]
