from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    website = models.URLField(blank=True) 
    picture = models.ImageField(upload_to='profile_images',blank=True) 
    
    def __str__(self): 
        return self.user.username
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    summary = models.TextField(blank=True)

    def __str__(self):
       return self.title    
    
