from django import forms
from django.contrib.auth.models import User 
from LibroLink.models import UserProfile, Review

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book_name', 'book_author', 'review_text', 'rating', 'book_image']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': 0.5}),
        }