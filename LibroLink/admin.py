from django.contrib import admin
from LibroLink.models import UserProfile
from .models import Review


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Review)
