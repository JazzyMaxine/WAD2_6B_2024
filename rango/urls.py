from django.urls import path
from rango import views

app_name = 'ramgo'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]