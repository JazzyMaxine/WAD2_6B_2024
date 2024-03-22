from django.urls import path
from LibroLink import views
from .views import reviews, ReviewListView
from .views import add_book


app_name = 'LibroLink'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('reviews/', views.reviews, name='reviews'),
    path('reviews/list/', ReviewListView.as_view(), name='review-list'), 
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete-review'),
    path('reviews/edit/<int:pk>/', views.ReviewUpdateView.as_view(), name='edit-review'),

    path('restricted/', views.restricted, name='restricted'),

    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.public_profile, name='user_profile'),

    path('search/', views.book_search, name='book_search'),
    path('help_support/', views.help_support, name='help_support'),
    path('privacy/', views.privacy, name='privacy'),

    path('books/', views.books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('featured/', views.featured, name='featured'),

    path('friends/', views.friends_list, name='friends_list'),
    path('add_friend/', views.add_friend, name='add_friend'),
  
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('user_not_found/<str:username>/', views.user_not_found, name='user_not_found'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('profile/<str:username>/', views.public_profile, name='user_profile'),
    path('add_book/', views.add_book, name='add_book'),
    path('thank_you/', views.thank_you, name='thank_you'),
]

