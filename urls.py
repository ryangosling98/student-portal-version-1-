from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
]