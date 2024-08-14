from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=8000)
    starting_bid = models.PositiveIntegerField(default=0)
    addition_time = models.DateTimeField(default=timezone.now)
    image = models.URLField(default=None, blank=True, null=True)
    category = models.CharField(max_length=32, choices=CATEGORIES, default='electronics')
    
    def __str__(self):
        return f"ID: {self.id} ADDED AT: {self.addition_time} BY: {self.author.username}\nTITLE:\n{self.title}\nCATEGORY: {self.category}\nDESCRIPTION:\n{self.description}\nSTARTING BID: {self.starting_bid}\nIMAGE: {self.image}\n"

class Bid(models.Model):
    pass
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    likes = models.PositiveIntegerField(default=0)
        
    def __str__(self) -> str:
        return f"Comment by: {self.author.username}\n{self.content}\n"