from django import forms
from django.contrib.auth.models import User 
from LibroLink.models import UserProfile, Review, Book

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class AddFriendForm(forms.Form):
    username = forms.CharField(max_length=150, label='Friend Username')
        
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('book_name', 'book_author', 'review_text', 'rating', 'book_image')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'step': 0.5,
                'min': 0,    
                'max': 5,    
            }),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publish_date', 'category', 'cover_image']       