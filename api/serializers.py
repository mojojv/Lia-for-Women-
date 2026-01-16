"""
Serializers for REST API.
"""
from rest_framework import serializers
from users.models import CustomUser
from chatbot.models import ChatInteraction
from clinical.models import SymptomReport, Alert
from psychosocial.models import EmotionLog, Recommendation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser."""
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class ChatInteractionSerializer(serializers.ModelSerializer):
    """Serializer for chat interactions."""
    
    class Meta:
        model = ChatInteraction
        fields = ['id', 'message_text', 'bot_response', 'sentiment_flag', 'timestamp']
        read_only_fields = ['id', 'bot_response', 'sentiment_flag', 'timestamp']


class SymptomReportSerializer(serializers.ModelSerializer):
    """Serializer for symptom reports."""
    
    class Meta:
        model = SymptomReport
        fields = ['id', 'symptom_type', 'intensity', 'description', 'location', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class EmotionLogSerializer(serializers.ModelSerializer):
    """Serializer for emotion logs."""
    
    class Meta:
        model = EmotionLog
        fields = ['id', 'mood_score', 'anxiety_score', 'energy_score', 'pain_emotional_impact', 'notes', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for recommendations."""
    
    class Meta:
        model = Recommendation
        fields = ['id', 'recommendation_text', 'category', 'is_ai_generated', 'created_at']
        read_only_fields = ['id', 'is_ai_generated', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for alerts."""
    
    class Meta:
        model = Alert
        fields = ['id', 'alert_type', 'severity', 'message', 'is_resolved', 'created_at']
        read_only_fields = ['id', 'created_at']
