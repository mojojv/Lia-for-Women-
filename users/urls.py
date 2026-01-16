"""
URL configuration for users app.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard redirect
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
]
