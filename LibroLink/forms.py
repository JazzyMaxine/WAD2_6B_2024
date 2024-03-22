from django import forms
from django.contrib.auth.models import User 
from LibroLink.models import UserProfile, Review
from LibroLink.models import Book, Reading, Read
from LibroLink.models import BookCategory



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
        
class BookSubmissionForm(forms.ModelForm):
    READING_STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('read', 'Read'),
    ]
    status = forms.ChoiceField(choices=READING_STATUS_CHOICES, label="Reading Status")

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'author', 'publisher', 'image', 'category')