from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from LibroLink.models import Book, BookCategory, Category
from LibroLink.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from LibroLink.models import Friends, FriendRequest, UserProfile, User

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


# friend stuff
def add_friend(request, friend_id):
    if request.method == 'POST':
        friend = get_object_or_404(user, id=friend_id)
        user = request.user
        if user == friend:
            return JsonResponse({'success': False, 'error': 'You cannot add yourself as a friend.'})
        if Friends.objects.filter(userA=user, userB=friend).exists() or Friends.objects.filter(userA=friend, userB=user).exists():
            return JsonResponse({'success': False, 'error': 'This user is already your friend.'})
        Friends.objects.create(userA=user, userB=friend)
        Friends.objects.create(userA=friend, userB=user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def friends_list(request):
    user_profile = request.user.profile
    if user_profile:
        friends = user_profile.friends.all()
    else:
        friends = []

    return render(request, 'friends_list.html', {'friends': friends})

def send_friend_request(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.user == recipient:
        return redirect('profile')  # Redirect back to profile
    FriendRequest.objects.create(sender=request.user, recipient=recipient)
    return redirect('profile')  # Redirect back to profile after sending request

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
    friend_request.status = 'accepted'
    friend_request.save()
    return redirect('friend_requests')  # Redirect back to friend requests page after accepting request

def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('friend_requests')  # Redirect back to friend requests page after rejecting request

def friend_requests(request):
    pending_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    return render(request, 'friend_requests.html', {'pending_requests': pending_requests})





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
    
@login_required
def user_logout(request):
    logout(request)
    HttpResponse("You have successfully logged out :)")
    return redirect(reverse('LibroLink:index'))

@login_required
def restricted(request):
    return HttpResponse("NOPE!")

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
    return render(request, 'LibroLink/featured.html')
