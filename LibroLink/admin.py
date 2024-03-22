from django.contrib import admin
from LibroLink.models import UserProfile, Reading, Friends, FriendRequest
from LibroLink.models import Category
from LibroLink.models import Book
from .models import Review


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Reading)
admin.site.register(Friends)
admin.site.register(FriendRequest)
