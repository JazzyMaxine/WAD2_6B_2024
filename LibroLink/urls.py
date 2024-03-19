from django.urls import path
from LibroLink import views
from .views import reviews, ReviewListView


app_name = 'LibroLink'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
<<<<<<< Updated upstream
=======
    path('profile/', views.profile, name='profile'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/list/', ReviewListView.as_view(), name='review-list'), 
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete-review'),
    path('reviews/edit/<int:pk>/', views.ReviewUpdateView.as_view(), name='edit-review'),

>>>>>>> Stashed changes
]