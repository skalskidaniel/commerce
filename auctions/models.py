from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name='watched_by', blank=True)


class Listing(models.Model):
    CATEGORIES = {
    'electronics': 'Electronics',
    'fashion': 'Fashion',
    'house_garden': 'House & Garden',
    'babies': 'Babies',
    'beauty': 'Beauty',
    'health': 'Health',
    'culture_entertainment': 'Culture and Entertainment',
    'sports_hobby': 'Sports and Hobby',
    'cars': 'Cars',
    'real_estates': 'Real Estates',
    'services': 'Services',
    }
    
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_listings')
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=8000)
    starting_bid = models.PositiveIntegerField(default=0)
    current_bid = models.PositiveIntegerField(default=0)
    addition_time = models.DateTimeField(default=timezone.now)
    image = models.URLField(default=None, blank=True, null=True)
    category = models.CharField(max_length=32, choices=CATEGORIES, default='electronics')
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='won_auctions', default=None, blank=True, null=True)
    
    def __str__(self):
        return f"ID: {self.id} DATE: {self.addition_time.date()} BY: {self.author.username}\nTITLE: {self.title}\n"
    
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    addition_time = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=1)
    value = models.PositiveIntegerField(default=0)
    
    def clean(self):
        if self.value < self.listing.starting_bid:
            raise ValidationError({
                'value': f'Bid value must be greater or equal to the starting bid of {self.listing.starting_bid}.'
            })
        elif self.value <= self.listing.current_bid:
            raise ValidationError({
                'value': f'Bid value must be greater than current bid of {self.listing.current_bid}.'
            })
            
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.listing.current_bid = self.value
        self.listing.save()
        
    def __str__(self):
        return f"LISTING ID: {self.listing.id} DATE: {self.addition_time.date()} BY: {self.author.username} VALUE: {self.value}"
    
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    addition_time = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
        
    def __str__(self) -> str:
        return f"LISTING ID: {self.listing.id} DATE: {self.addition_time.date()} BY: {self.author.username}"