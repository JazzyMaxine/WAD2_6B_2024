from django.shortcuts import render
from django.http import HttpResponse
#from LibroLink.models import Book
#from LibroLink.models import Category
from LibroLink.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin




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
    template_name = 'LibroLink/reviews_list.html'  # might need to create this template
    context_object_name = 'reviews'
    paginate_by = 10  # Optional: want to paginate the reviews

    def get_queryset(self):
        """Optionally, you can filter the reviews or order them differently."""
        return Review.objects.order_by('-id')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this review.")
    if request.method == 'POST':  # Ensuring deletion is confirmed via POST request
        review.delete()
        return redirect('LibroLink:review-list')  # Redirecting to the list of reviews after deletion
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
def profile(request):
    user_profile = request.user.userprofile
    context = {
        'user': request.user,
        'user_profile': user_profile
    }
    return render(request, 'LibroLink/profile.html', context)