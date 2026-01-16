"""
URL configuration for psychologist app.
"""
from django.urls import path
from . import views

app_name = 'psychologist'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/<int:patient_id>/', views.patient_emotional_detail, name='patient_detail'),
]
