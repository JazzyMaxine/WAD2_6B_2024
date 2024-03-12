from django.db import models
from django.contrib.auth.models import User

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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Friends(models.Model):
    userA = models.ForeignKey(User, on_delete=models.CASCADE)
    userB = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userA.username + ", " + self.userB.username
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    timeSent = models.DateTimeField()
    content = models.CharField(max_length = 2000)

    def __str__(self):
        return self.content
    
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    timePosted = models.DateTimeField()
    content = models.CharField(max_length = 4000)

    def __str__(self):
        return self.content
    
class Book(models.Model):
    isbn = models.CharField(max_length = 13, unique = True)
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    publisher = models.CharField(max_length = 200)

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