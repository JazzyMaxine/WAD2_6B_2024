from django.shortcuts import render
from django.http import HttpResponse
from LibroLink.models import Book
from LibroLink.models import Category
from LibroLink.forms import UserForm,UserProfileForm, AddFriendForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from LibroLink.models import Friends
from django.contrib.auth.decorators import login_required
from LibroLink.models import UserProfile
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'LibroLink/index.html')


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
    books = Book.objects.all().order_by('title')  
    return render(request, 'LibroLink/books.html',{'books': books})


@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  

    return render(request, 'LibroLink/profile.html', {'user_profile': user_profile})



@login_required
def friends_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    friends = Friends.objects.filter(userA=user_profile.user) | Friends.objects.filter(userB=user_profile.user)
    friends_list = []
    for friend in friends:
        if friend.userA == user_profile.user:
            friends_list.append(friend.userB)
        else:
            friends_list.append(friend.userA)
    context = {
        'friends_list': friends_list
    }
    return render(request, 'LibroLink/friends.html', context)


@login_required
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                friend_profile = UserProfile.objects.get(user__username=username)
                user_profile = UserProfile.objects.get(user=request.user)
                if Friends.objects.filter(userA=user_profile.user, userB=friend_profile.user).exists() or \
                        Friends.objects.filter(userA=friend_profile.user, userB=user_profile.user).exists():
                    messages.error(request, 'You are already friends with {}'.format(username))
                elif user_profile.user == friend_profile.user:
                    messages.error(request, 'You cannot add yourself as a friend')
                else:
                    Friends.objects.create(userA=user_profile.user, userB=friend_profile.user)
                    messages.success(request, 'Friend request sent to {}'.format(username))
            except UserProfile.DoesNotExist:
                messages.error(request, 'User with username {} does not exist'.format(username))
    else:
        form = AddFriendForm()
    return render(request, 'LibroLink/add_friend.html', {'form': form})