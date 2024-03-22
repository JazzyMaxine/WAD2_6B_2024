from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review
from .forms import ReviewForm
from django.urls import reverse

# Create your tests here.




class ReviewModelTests(TestCase):

    def test_review_creation(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='12345')
        
        # Create and save a new review
        review = Review.objects.create(
            user=user, 
            book_name="Test Book",
            book_author="Test Author",
            review_text="This is a test review.",
            rating=5,
        )
        
        # Check that the review has been correctly created
        self.assertEqual(review.book_name, "Test Book")
        self.assertEqual(review.book_author, "Test Author")
        self.assertEqual(review.review_text, "This is a test review.")
        self.assertEqual(review.rating, 5)
        
        
from .forms import ReviewForm

class ReviewFormTests(TestCase):

    def test_valid_form_submission(self):
        form_data = {
            'book_name': 'Test Book',
            'book_author': 'Test Author',
            'review_text': 'Test review text.',
            'rating': '5',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_submission(self):
        form_data = {
            'book_name': '',
            'book_author': 'Test Author',
            'review_text': 'Test review text.',
            'rating': '5',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        
from django.urls import reverse

class ReviewViewTests(TestCase):

    def setUp(self):
        # Set up data for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.review_url = reverse('LibroLink:reviews')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.review_url)
        self.assertRedirects(response, '/LibroLink/login/?next=/LibroLink/reviews/')

    def test_logged_in_user_can_access_review_page(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.review_url)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)