from django.test import TestCase
from django.contrib.auth.models import User
from LibroLink.models import Review
from LibroLink.forms import ReviewForm, BookSubmissionForm
from django.urls import reverse
from LibroLink.models import Book



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
        
class BookModelTests(TestCase):

    def test_book_creation(self):
        # Create a book instance
        book = Book.objects.create(
            isbn="1234567890123",
            title="Test Book Title",
            author="Test Author",
            publisher="Test Publisher",
        )

        # Check that the book has been correctly created
        self.assertEqual(book.isbn, "1234567890123")
        self.assertEqual(book.title, "Test Book Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.publisher, "Test Publisher")


class BookSubmissionFormTests(TestCase):

    def test_valid_book_form_submission(self):
        form_data = {
            'isbn': '1234567890123',
            'title': 'Test Book Title',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'status': 'reading',
        }
        form = BookSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_book_form_submission(self):
        form_data = {
            'isbn': '',  # ISBN is required
            'title': 'Test Book Title',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'status': 'reading',
        }
        form = BookSubmissionForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddBookViewTests(TestCase):

    def setUp(self):
        # Set up data for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.add_book_url = reverse('LibroLink:add_book')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.add_book_url)
        self.assertRedirects(response, '/LibroLink/login/?next=/LibroLink/add_book/')

    def test_logged_in_user_can_access_add_book_page(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.add_book_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'LibroLink/add_book.html')

    def test_form_error_on_invalid_book_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.add_book_url, {
            'isbn': '',  # Missing ISBN
            'title': 'Test Book Title',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'status': 'reading',
        })
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'isbn', 'This field is required.')

    def test_successful_book_addition(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.add_book_url, {
            'isbn': '1234567890123',
            'title': 'Test Book Title',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'status': 'reading',
        }, follow=True)
        self.assertTrue(Book.objects.filter(title='Test Book Title').exists())
        self.assertRedirects(response, reverse('LibroLink:thank_you'))
        
class FriendRequestTests(TestCase):

    def setUp(self):
        # Create a user that will attempt to send a friend request
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Login the user
        self.client.login(username='testuser', password='12345')
        # URL for sending friend requests
        self.add_friend_url = reverse('LibroLink:add_friend')

   