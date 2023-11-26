from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("listing/<int:listing_id>", views.listing, name = "listing"),
    path("<int:listing_id>/bid", views.bid, name = "bid"),
    path("<int:listing_id>/end", views.endAuction, name = "end"),
    path("<int:listing_id>/addComment", views.addComment, name = "addComment"),
    path("<int:listing_id>/delete", views.deleteListing, name = "delete"),
    path("<int:listing_id>/add", views.addToWatchlist, name = "add"),
    path("<int:user_id>/watchlist", views.watchlist, name = "watchlist"),
    path("categories", views.categories, name = "categories"),
    path("category/<int:category_id>", views.category, name = "by_category"),
    path("<int:user_id>/watchlist/delete", views.deleteFromWatchlist, name="deleteFromWatchlist"),
    path("closedListings", views.closedListings, name="closed"),
    path("closedListings/<int:listing_id>", views.closedListing, name="closedListing")
]
