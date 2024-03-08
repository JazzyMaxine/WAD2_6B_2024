from django.urls import path
from LibroLink import views

app_name = 'LibroLink'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
]