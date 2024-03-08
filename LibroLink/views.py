from django.shortcuts import render
from django.http import HttpResponse
from LibroLink.models import Book
from LibroLink.models import Category

def index(request):
    return render(request, 'LibroLink/index.html')


def profile(request):
    
    category_list = Category.objects.order_by('-activity')[:5]
    book_list = Book.objects.order_by('-readingOrder')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['book'] = book_list

    return render(request, 'LibroLink/profile.html', context=context_dict)