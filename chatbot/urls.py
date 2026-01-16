"""
URL configuration for chatbot app.
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_interface, name='interface'),
    path('send/', views.send_message, name='send_message'),
    path('history/', views.chat_history, name='history'),
    path('voice/upload/', views.upload_voice_memo, name='upload_voice'),
]
