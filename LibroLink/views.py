
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from LibroLink.models import Book, BookCategory, Category, Page, Featured
from LibroLink.models import Category
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from LibroLink.models import Friends, FriendRequest, UserProfile, User
from django.db.models import Count, Q
from LibroLink.forms import UserForm, UserProfileForm, AddFriendForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from LibroLink.forms import UserForm,UserProfileForm, AddFriendForm
from .forms import BookSubmissionForm
from .models import Reading, Read
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import BookSubmissionForm
from django.db.models import Q
from django.shortcuts import render

User = get_user_model()

# Create your views here.
def index(request):
    return render(request, 'LibroLink/index.html')
    return render(request, 
                  'LibroLink/register.html', 
                  context = {'user_form':user_form, 
                             'profile_form':profile_form, 
                             'registered':registered})

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
def reviews(request):
    form = ReviewForm()
    context = {
        'form': form,
        'rating_choices': ['5', '4', '3', '2', '1']
    }

    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  
            review.save()
            return redirect(reverse('LibroLink:review-list'))  
        else:
            print(form.errors, form.errors)  
    
    return render(request, 'LibroLink/reviews.html', context)



class ReviewListView(ListView):
    model = Review
    template_name = 'LibroLink/reviews_list.html'  
    context_object_name = 'reviews'
    paginate_by = 10  

    def get_queryset(self):
        """Optionally, you can filter the reviews or order them differently."""
        return Review.objects.order_by('-id')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this review.")
    if request.method == 'POST':  
        review.delete()
        return redirect('LibroLink:review-list')  
    else:
        return render(request, 'LibroLink/confirm_delete.html', {'review': review})
    
class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['book_name', 'book_author', 'review_text', 'rating', 'book_image']
    template_name = 'LibroLink/edit_review.html'
    success_url = reverse_lazy('LibroLink:review-list')

    def get_queryset(self):
        """Allow users to edit only their own reviews unless they are superusers."""
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset

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
    books = Book.objects.all().annotate(num_readers=Count('reading')).order_by('num_readers')[:10]
    context = {'books': books}
    return render(request, 'LibroLink/featured.html', context=context)

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
        books = Book.objects.filter(
            Q(isbn__icontains=query) | 
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(publisher__icontains=query)
        )
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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        friends = Friends.objects.filter(Q(userA=user_profile.user) | Q(userB=user_profile.user))
        friends_set = set()
        for friend in friends:
            if friend.userA == user_profile.user:
                friends_set.add(friend.userB)
            else:
                friends_set.add(friend.userA)

        friends_list = list(friends_set)

        pending_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')

        context = {
            'friends_list': friends_list,
            'pending_requests': pending_requests,
        }
    except ObjectDoesNotExist:
        context = {'friends_list': []}
    return render(request, 'LibroLink/friends.html', context)


@login_required
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            sender = request.user
            try:
                recipient = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('LibroLink:user_not_found', args=(username,)))
            
            existing_request = FriendRequest.objects.filter(sender=sender, recipient=recipient).exists()
            if existing_request:
                messages.error(request, f"Friend request already sent to {username}")
            elif recipient == sender:
                messages.error(request, "You cannot send a friend request to yourself")
            else:
                FriendRequest.objects.create(sender=sender, recipient=recipient)
                messages.success(request, f"Friend request sent to {username}")
                return redirect('LibroLink:add_friend')
    else:
        form = AddFriendForm()
    return render(request, 'LibroLink/add_friend.html', {'form': form})

def user_not_found(request, username):
    return render(request, 'LibroLink/user_not_found.html', {'username': username})

def friend_requests(request):
    received_requests = FriendRequest.objects.filter(recipient=request.user, status='pending')
    return render(request, 'LibroLink/friend_requests.html', {'received_requests': received_requests})

def accept_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
    friend_request.status = 'accepted'
    friend_request.save()

    Friends.objects.create(userA=friend_request.sender, userB=request.user)
    Friends.objects.create(userA=request.user, userB=friend_request.sender)

    messages.success(request, 'Friend request accepted.')
    return redirect('LibroLink:friends_list')

def reject_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    messages.success(request, 'Friend request rejected.')
    return redirect('LibroLink:friends_list')

def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    user_profile = get_object_or_404(UserProfile, user=user)

    context = {'user': user, 'user_profile': user_profile}
    return render(request, 'LibroLink/publicProfile.html', context)

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  
            book.save()  
            status = form.cleaned_data['status']
            if status == 'reading':
                Reading.objects.create(user=request.user, book=book)
            else:  
                Read.objects.create(user=request.user, book=book, dateFinished=datetime.now())
            return redirect('LibroLink:thank_you')  
    else:
        form = BookSubmissionForm()
    return render(request, 'LibroLink/add_book.html', {'form': form})


@login_required
def thank_you(request):
    return render(request, 'LibroLink/thank_you.html')

def books(request):
    all_books = Book.objects.all().order_by('title')  
    return render(request, 'LibroLink/library.html', {'books': all_books})