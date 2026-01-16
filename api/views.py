"""
Views for REST API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from chatbot.models import ChatInteraction
from clinical.models import SymptomReport
from psychosocial.models import EmotionLog, Recommendation
from chatbot.services import chat_service

from .serializers import (
    ChatInteractionSerializer,
    SymptomReportSerializer,
    EmotionLogSerializer,
    RecommendationSerializer
)


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint for chat interactions.
    Supports creating new messages and retrieving history.
    """
    serializer_class = ChatInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatInteraction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Process message through chat service
        message = serializer.validated_data['message_text']
        result = chat_service.process_message(message, self.request.user.first_name)
        
        # Save with bot response
        serializer.save(
            user=self.request.user,
            bot_response=result['response'],
            sentiment_flag=result['sentiment'],
            risk_keywords_detected=result['risk_keywords']
        )


class SymptomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for symptom reports.
    """
    serializer_class = SymptomReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SymptomReport.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user, reported_via='FORM')


class EmotionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for emotion logs.
    """
    serializer_class = EmotionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmotionLog.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for recommendations (read-only for patients).
    """
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Recommendation.objects.filter(
            patient=self.request.user,
            is_active=True
        )
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark recommendation as completed."""
        recommendation = self.get_object()
        recommendation.patient_completed = True
        recommendation.save()
        return Response({'status': 'completed'})
