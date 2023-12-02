from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    category_title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_title}"

class Listing(models.Model):
    listing_title = models.CharField(max_length=64)
    listing_description = models.TextField(null=True, blank=True)
    img_url = models.CharField(max_length = 150)
    starting_bid = models.FloatField()
    lister = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listing")
    # lister = models.CharField(max_length = 64)
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categorizing", null=True, blank=True)
    watchers = models.ManyToManyField(User, blank = True, related_name = "watchlist")
    highest_bid = models.FloatField(default = 0)
    current_price = models.FloatField(null=True, blank=True)
    buyer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bought", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_listed = models.DateField(default=datetime.date.today, blank = True)

    def __str__(self):
        return f"{self.listing_title}"

class Bid(models.Model):
    bid_price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bidding")
    date_of_bid = models.DateField(default=datetime.date.today, blank = True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="biddings", default=None)

    def __str__(self):
        return f"{self.bid_price}({self.bidder})"

class Comment(models.Model):
    content = models.TextField(null=True, blank=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    date_commented = models.DateField(default=datetime.date.today, blank = True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=None)

    def __str__(self):
        return f"Comment # {self.id} - {self.commenter}"

'''
This is a limited-edition broomstick, used by many Quidditch players. AND... wait for it... this specific broomstick was used by The Boy who Lived himself, Harry MF Potter!! so yeah... DEFINITELY NOT FOR MUGGLES.
https://static.wikia.nocookie.net/harrypotter/images/0/0f/Nimbus_2000_1.jpg/revision/latest?cb=20150530185551
'''