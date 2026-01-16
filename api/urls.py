"""
URL configuration for API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()
router.register(r'chat', views.ChatViewSet, basename='chat')
router.register(r'symptoms', views.SymptomViewSet, basename='symptom')
router.register(r'emotions', views.EmotionViewSet, basename='emotion')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='token_auth'),
]
