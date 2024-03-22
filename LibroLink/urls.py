from django.urls import path
from LibroLink import views
from .views import reviews, ReviewListView


app_name = 'LibroLink'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/list/', ReviewListView.as_view(), name='review-list'), 
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete-review'),
    path('reviews/edit/<int:pk>/', views.ReviewUpdateView.as_view(), name='edit-review'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.book_search, name='book_search'),
    path('help_support/', views.help_support, name='help_support'),
    path('privacy/', views.privacy, name='privacy'),
    path('books/', views.books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('featured/', views.featured, name='featured'),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    # path('bookshelf/', views.bookshelf, name='bookshelf'),
    # path('settings/', views.accountSettings, name='settings'),
    path('friends/', views.friends_list, name='friends_list'),
    # path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]