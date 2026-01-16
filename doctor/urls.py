"""
URL configuration for doctor app.
"""
from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
]
