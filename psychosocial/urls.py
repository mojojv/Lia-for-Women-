"""
URL configuration for psychosocial app.
"""
from django.urls import path
from . import views

app_name = 'psychosocial'

urlpatterns = [
    # Patient views
    path('checkin/', views.emotion_checkin, name='emotion_checkin'),
    path('recommendations/', views.my_recommendations, name='my_recommendations'),
    path('consent/', views.manage_consent, name='manage_consent'),
    path('history/', views.emotion_history, name='emotion_history'),
    
    # Psychologist views
    path('patient/<int:patient_id>/emotions/', views.patient_emotions, name='patient_emotions'),
    path('patient/<int:patient_id>/recommend/', views.create_recommendation, name='create_recommendation'),
]
