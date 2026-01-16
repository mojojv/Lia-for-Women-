"""
URL configuration for clinical app.
"""
from django.urls import path
from . import views

app_name = 'clinical'

urlpatterns = [
    # Patient views
    path('report/', views.report_symptom, name='report_symptom'),
    path('my-symptoms/', views.my_symptoms, name='my_symptoms'),
    
    # Doctor views
    path('patient/<int:patient_id>/symptoms/', views.patient_symptoms, name='patient_symptoms'),
    path('patient/<int:patient_id>/timeline/', views.patient_timeline, name='patient_timeline'),
    path('alert/<int:alert_id>/resolve/', views.resolve_alert, name='resolve_alert'),
]
