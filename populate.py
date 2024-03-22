import os
from datetime import datetime
from django.utils import timezone
import pytz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_6B_2024.settings')

import django
django.setup()
from LibroLink.models import *

def populate():

    book_categories = [
        {
            
        }
    ]

    books = [
        {
            'isbn':'9780450054655',
            'title':'Dune',
            'author':'Frank Herbert',
            'publisher':'New English Library Ltd'
        },
        {
            'isbn':'9780141439471',
            'title':'Frankenstein: Or the Modern Prometheus',
            'author':'Mary Shelley',
            'publisher':'Penguin Classics'
        },
        {
            'isbn':'9780141182636',
            'title':'The Great Gatsby',
            'author':'F. Scott Fitzgerald',
            'publisher':'Penguin Classics'
        },
        {
            'isbn':'9781087964669',
            'title':'The Great Gatsby: But Nick has Scoliosis',
            'author':'Dick Cody Heese',
            'publisher':'Dick Cody Heese'
        },
        {
            'isbn':'9780385339032',
            'title':'Screenplay: The Foundations of Screenwriting',
            'author':'Syd Field',
            'publisher':'Random House Publishing Group'
        }
    ]

    users = [
        {
            'username':'SaulGoodman',
            'password':'b3tt3rc4lls4ul',
        },
        {
            'username':'RustCohle',
            'password':'t1me1s4fl4tc1rcle',
        },
        {
            'username':'ClarkKent',
            'password':'n0tSup3rman',
        },
        {
            'username':'SarahConnor',
            'password':'n0Futur3butwh4tw3m4k3f0r0urs3lv3s',
        },
        {
            'username':'AnakinSkywalker',
            'password':'j3d1ord3r'
        }
    ]

    readings = [
        {
            'user':'RustCohle',
            'book':'9780450054655',
        },
    ]

    reviews = [
        {
            'user':'AnakinSkywalker',
            'book':'9780450054655',
            'text':'Too much sand.',
            'rating':1
        },
        {
            'user':'SaulGoodman',
            'book':'9780141439471',
            'text':'Wow, he could have just not done all that, huh.',
            'rating':4
        }
    ]

    friends = [
        {
            'a':'ClarkKent',
            'b':'SarahConnor',
            'date':datetime(2023,3,20,12,6,57,4563, tzinfo=pytz.UTC),
        },
    ]

    friend_requests = [
        {
            'a':'SaulGoodman',
            'b':'RustCohle',
            'date':datetime(2023,3,20,12,6,57,4563, tzinfo=pytz.UTC),
            'status':'pending'
        },
    ]

    for user in users:
        u = add_user(user['username'], user['password'])

    for friend in friends:
        f = add_friend(friend['a'], friend['b'], friend['date'])

    for friend_request in friend_requests:
        frq = add_friend_request(friend_request['a'], friend_request['b'], friend_request['status'], friend_request['date'])

    for book in books:
        b = add_book(book['isbn'], book['title'], book['author'], book['publisher'])
    
    for reading in readings:
        r = add_reading(reading['user'], reading['book'])
    
    for review in reviews:
        r = add_review(review['user'], review['book'], review['text'], review['rating'])

def add_user(name, password):
    try:
        u = User.objects.create_user(
            username=name,password=password
        )
        u.save()
        return u
    except:
        return None

def add_friend(a, b, date):
    try:
        f = Friends.objects.get_or_create(userA = User.objects.filter(username = a)[0], userB = User.objects.filter(username = b)[0], date_established=date)[0]
        f.save()
        return f
    except:
        return None

def add_friend_request(a, b, status, date):
    frq = FriendRequest.objects.get_or_create(sender=User.objects.filter(username = a)[0], recipient=User.objects.filter(username = b)[0], status=FriendRequest.STATUS_CHOICES[0], timestamp=date)[0]
    frq.save()
    return frq

def add_book(isbn, title, author, publisher):
    b = Book.objects.get_or_create(isbn = isbn)[0]
    b.title = title
    b.author = author
    b.publisher = publisher
    b.save()
    return b

def add_user_profile(username):
    u = UserProfile.objects.get_or_create(user = User.objects.filter(username = username)[0])[0]
    u.save()
    return u


def add_reading(username, book):
    r = Reading.objects.get_or_create(user=User.objects.filter(username = username)[0], book=Book.objects.filter(isbn=book)[0])[0]
    r.save()
    return r

def add_review(username, book, text, rating):
    r = Review.objects.get_or_create(user=User.objects.filter(username = username)[0], book_name=Book.objects.filter(isbn=book)[0].title, book_author=Book.objects.filter(isbn=book)[0].author, review_text=text, rating=rating)[0]
    r.save()
    return r

if __name__ == "__main__":
    populate()
