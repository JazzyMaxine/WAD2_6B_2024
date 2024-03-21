from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from LibroLink.models import Book,BookCategory, Page, Featured
from LibroLink.models import Category
from LibroLink.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Count
from LibroLink.models import Friends

# Create your views here.
def index(request):
    return render(request, 'LibroLink/index.html')

def profile(request):
    
    category_list = Category.objects.order_by('-likes')[:5]
    book_list = Book.objects.order_by('-title')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['book'] = book_list

    return render(request, 'LibroLink/profile.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 
                  'LibroLink/register.html', 
                  context = {'user_form':user_form, 
                             'profile_form':profile_form, 
                             'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('LibroLink:index'))
            else:
                return HttpResponse("Your book finder account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'LibroLink/login.html')


def show_category(request, category_name_slug):
    
    context_dict = {}

    try:

        category = Category.objects.get(slug=category_name_slug)
        books = Book.objects.filter(category=category)
        context_dict['books'] = books
        context_dict['category'] = category
    
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['books'] = None

    
    return render(request, 'LibroLink/category.html', context=context_dict)


def book_search(request):
    query = request.GET.get('searchQuery') 
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = None 
    return render(request, 'LibroLink/search_results.html', {'books': books})


def help_support(request):
    return render(request, 'LibroLink/help_support.html')

def privacy(request):
    return render(request, 'LibroLink/privacy.html')

def books(request):
    categories = BookCategory.objects.all()
    return render(request, 'LibroLink/books.html', {'categories': categories})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'LibroLink/book_detail.html', {'book': book})

def featured(request):
    pages = Page.objects.all().annotate(num_followers=Count('followers')).order_by('num_followers')[:5]
    books = {}
    for featured in Featured.objects.all():
        if featured.page in pages:
            if not books.has_key(featured.page):
                books[featured.page] = []
            books[featured.page].append(featured.book)
    context = {'pages': pages,
               'books': books}
    return render(request, 'LibroLink/featured.html', context=context)