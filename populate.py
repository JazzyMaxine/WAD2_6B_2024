import os
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

    users = [
        {
            'username':'LR-II',
            #'password':'unsafePassword123',
            'email':'lucaskennington@gmail.com',
            'first_name':'Lucas',
            'last_name':'Kennington'
        },
        {
            'username':'rCalifornia12',
            #'password':'lizardKing76',
            'email':'robertcalifornia@dundermifflin.org',
            'first_name':'Bob',
            'last_name':'Kamazakis'
        }
    ]



    pages = [
        {
            'uniqueID':'1',
            'name':'Books that cure my motion sickness',
            'admin':'rCalifornia12'
        },
        {
            'uniqueID':'2',
            'name':'Every book is just a remix of the dictionary',
            'admin':'LR-II'
        }
    ]

    for book, book_data in books.items():
        b = add_book(book)
    
    for user, user_data in users.items():
        u = add_user(user)

    for page, page_data in pages.items():
        p = add_page(page)

    def add_book(isbn, title, author, publisher):
        b = Book.objects.get_or_create(isbn = isbn)[0]
        b.title = title
        b.author = author
        b.isbn = isbn
        b.save()
        return b
    
    
    
