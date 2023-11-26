from django.contrib import admin
from . models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_title", "listing_category", "lister", "buyer", "highest_bid", "is_active")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)