from django.shortcuts import render
from django.http import HttpResponse
# from LibroLink.models import Book
# from LibroLink.models import Category
from LibroLink.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'LibroLink/index.html')

def profile(request):
    
    category_list = Category.objects.order_by('-activity')[:5]
    book_list = Book.objects.order_by('-readingOrder')[:5]

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

