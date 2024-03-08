from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Book
from rango.models import Category

def index(request):
    return render(request, 'rango/index.html')


def profile(request):
    
    category_list = Category.objects.order_by('-activity')[:5]
    book_list = Book.objects.order_by('-readingOrder')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['book'] = book_list

    return render(request, 'rango/profile.html', context=context_dict)