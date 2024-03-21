from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):

    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    website = models.URLField(blank=True) 
    picture = models.ImageField(upload_to='profile_images',blank=True) 
    
    def __str__(self): 
        return self.user.username
    
class Page(models.Model):
    uniqueID = models.BigIntegerField(default = 0, unique = True)
    name = models.CharField(max_length = 128)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Contributors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
##class Friends(models.Model):
##<<<<<<< HEAD
#3    userA = models.ForeignKey(User, related_name = 'userA', on_delete=models.CASCADE)
#    userB = models.ForeignKey(User, related_name = 'userB', on_delete=models.CASCADE)
#=======
#    userA = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user_a")
#    userB = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user_b")
#    date_established = models.DateTimeField(auto_now_add=True)
#>>>>>>> main

#    class Meta:
#        unique_together = ('userA', 'userB')
        
#    def __str__(self):
#        return self.userA.username + ", " + self.userB.username
    
#class Message(models.Model):
#    sender = models.ForeignKey(User, related_name = 'userC', on_delete=models.CASCADE)
#    receiver = models.ForeignKey(User, related_name = 'userD', on_delete=models.CASCADE)
#    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
#    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_receiver")
#    timeSent = models.DateTimeField()
#    content = models.CharField(max_length = 2000)

#    def __str__(self):
#        return self.content
    
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    timePosted = models.DateTimeField()
    content = models.CharField(max_length = 4000)

    def __str__(self):
        return self.content
    
class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BookCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn = models.CharField(max_length = 13, unique = True)
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    publisher = models.CharField(max_length = 200)
    category = models.ForeignKey(BookCategory, related_name='books', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Featured(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.page.name + ": " + self.book.title
    
class Reading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ": " + self.book.title
    
class Read(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    dateFinished = models.DateTimeField()

    def __str__(self):
        return self.self.user.username + ": " + self.book.title
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)
    content = models.CharField(max_length = 2000)

    def __str__(self):
        return self.content