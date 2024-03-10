from django.urls import path
from LibroLink import views

app_name = 'LibroLink'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('bookshelf/', views.bookshelf, name='bookshelf'),
    path('settings/', views.accountSettings, name='settings'),
    path('friends/', views.friends, name='friends'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]