import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_6B_2024.settings')

import django
django.setup()
from LibroLink.models import *

def populate():
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
        }
    ]

    user_profiles = [
        {
            'user':'lucas'
        },
        {
            'user':'nathan'
        }
    ]

    pages = [
        {
            'uniqueID':'1',
            'name':'Books that cure my motion sickness',
            'admin':'lucas'
        },
        {
            'uniqueID':'2',
            'name':'Every book is just a remix of the dictionary',
            'admin':'nathan'
        }
    ]

    contributors = [
        {
            'user':'lucas',
            'page':'1'
        },
        {
            'user':'nathan',
            'page':'2'
        }
    ]

    followers = [
        {
            'user':'nathan',
            'page':'1'
        }
    ]

    friends = [
        {
            'userA':'lucas',
            'userB':'nathan'
        }
    ]

    messages = [
        {
            'sender':'lucas',
            'receiver':'nathan',
            'timeSent':datetime(2023,3,20,12,5,57,5555),
            'content':'Are we real?'
        },
        {
            'sender':'nathan',
            'receiver':'lucas',
            'timeSent':datetime(2023,3,20,12,6,57,4563),
            'content':'No, we are merely vessels for example data. Sorry.'
        },
        {
            'sender':'lucas',
            'receiver':'nathan',
            'timeSent':datetime(2023,3,20,12,7,57,7643),
            'content':'Shame.'
        }
    ]

    blogPosts = [
        {
            'user':'lucas',
            'page':'1',
            'timePosted':datetime(2023,3,20,12,7,57,7643),
            'content':'Ever heard of cheese? Good stuff. You can get yellow cheese, white cheese, blue cheese, red cheese. Probably purple cheese if you look close enough. Man, cheese is good.'
        },
        {
            'user':'nathan',
            'page':'2',
            'timePosted':datetime(2023,3,20,12,6,57,4563),
            'content':'I am afraid of big bugs. They keep bothering me.'
        }
    ]

    featureds = [
        {
            'book':'9780450054655',
            'page':'1'
        },
        {
            'book':'9780141182636',
            'page':'2'
        }
    ]

    readings = [
        {
            'user':'lucas',
            'book':'9780141182636'
        },
        {
            'user':'nathan',
            'book':'9780450054655'
        }
    ]

    reads = [
        {
            'user':'lucas',
            'book':'9780141439471',
            'dateFinished':datetime(2023,3,20,12,6,57,4563)
        }
    ]

    reviews = [
        {
            'reviewer':'lucas',
            'book':'9780141439471',
            'rating':'5',
            'content':'Wow, he really could have just not done that, huh.'
        },
        {
            'reviewer':'nathan',
            'book':'9780141182636',
            'rating':'4',
            'content':'Muppets version when?'
        },
        {
            'reviewer':'nathan',
            'book':'9780450054655',
            'rating':'1',
            'content':'Not enough sand.'
        },
    ]


    for book in books:
        b = add_book(book['isbn'], book['title'], book['author'], book['publisher'])

    """
    for page in pages:
        p = add_page(page['uniqueID'], page['name'], page['admin'])
    """

    for contributor in contributors:
        c = add_contributor(contributor['user'], contributor['page'])

    for follower in follower:
        f = add_followers(follower['user'], follower['page'])

    for friend in friends:
        f = add_friends(friend['userA'], friend['userB'])

    for message in messages:
        m = add_messages(message['sender'], message['receiver'], message['timeSent'], message['content'])

    for blogPost in blogPosts:
        b = add_blog_post(blogPost['user'], blogPost['page'], blogPost['timePosted'], blogPost['content'])

    for featured in featureds:
        f = add_featured(featured['book'], featured['page'])

    for reading in readings:
        r = add_reading(reading['user'], reading['book'])

    for read in reads:
        r = add_read(read['user'], read['book'], read['dateFinished'])

    for review in reviews:
        r = add_review(review['reviewer'], review['book'], review['rating'], review['content'])

def add_book(isbn, title, author, publisher):
    b = Book.objects.get_or_create(isbn = isbn)[0]
    b.title = title
    b.author = author
    b.publisher = publisher
    b.save()
    return b

def add_page(uniqueID, name, admin):
    p = Page.objects.get_or_create(uniqueID=uniqueID)[0]
    p.name = name
    p.admin = admin
    p.save()
    return p

def add_contributor(user, page):
    c = Contributors.objects.get_or_create(user = User.objects.filter(username = user)[0], page = Page.objects.filter(uniqueID = page))[0]
    c.save()
    return c

def add_followers(user, page):
    f = Followers.objects.get_or_create(user = User.objects.filter(username = user), page = Page.objects.filter(uniqueID = page))[0]
    f.save()
    return f

def add_friends(userA, userB):
    f = Friends.objects.get_or_create(userA = User.objects.filter(username = userA), userB = User.objects.filter(username = userB))[0]
    f.save()
    return f

def add_messages(sender, receiver, timeSent, content):
    m = Message.objects.get_or_create(sender = User.objects.filter(username = sender), receiver = User.objects.filter(username = receiver), timeSent = timeSent)[0]
    m.content = content
    m.save()
    return m

def add_blog_post(user, page, timePosted, content):
    b = BlogPost.objects.get_or_create(user = User.objects.filter(username = user), page = Page.objects.filter(uniqueID = page), timePosted = timePosted)[0]
    b.content = content
    b.save()
    return b

def add_featured(book, page):
    f = Featured.objects.get_or_create(book = Book.objects.filter(isbn = book), page = Page.objects.filter(uniqueID = page))[0]
    f.save()
    return f

def add_reading(user, book):
    r = Reading.objects.get_or_create(user = User.objects.filter(username = user), book = Book.objects.filter(isbn = book))[0]
    r.save()
    return r

def add_read(user, book, dateFinished):
    r = Read.objects.get_or_create(user = User.objects.filter(username = user), book = Book.objects.filter(isbn = book), dateFinished = dateFinished)[0]
    r.save()
    return r

def add_review(reviewer, book, rating, content):
    r = Review.objects.get_or_create(reviewer = User.objects.filter(username = reviewer), book = Book.objects.filter(isbn = book))[0]
    r.rating = rating
    r.content = content
    r.save()
    return r

if __name__ == "__main__":
    populate()
