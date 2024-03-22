from django.contrib import admin
from LibroLink.models import UserProfile
<<<<<<< Updated upstream

# Register your models here.
admin.site.register(UserProfile)
=======
from LibroLink.models import Category
from LibroLink.models import Book
from LibroLink.models import BookCategory
from .models import Review


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookCategory)

>>>>>>> Stashed changes
