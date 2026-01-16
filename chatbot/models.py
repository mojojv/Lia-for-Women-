"""
Models for chatbot module.
Stores chat interactions and voice memos.
"""
from django.db import models
from django.conf import settings
# from simple_history.models import HistoricalRecords  # Temporarily disabled


class ChatInteraction(models.Model):
    """
    Stores individual chat messages and bot responses.
    Includes sentiment analysis and risk flagging.
    """
    SENTIMENT_CHOICES = [
        ('NEUTRAL', 'Neutral'),
        ('POSITIVE', 'Positivo'),
        ('CONCERN', 'Preocupación'),
        ('ALERT', 'Alerta'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_interactions',
        verbose_name='Usuario'
    )
    
    message_text = models.TextField(
        verbose_name='Mensaje del usuario'
    )
    
    bot_response = models.TextField(
        verbose_name='Respuesta de Lia'
    )
    
    sentiment_flag = models.CharField(
        max_length=10,
        choices=SENTIMENT_CHOICES,
        default='NEUTRAL',
        verbose_name='Indicador de sentimiento'
    )
    
    risk_keywords_detected = models.JSONField(
        default=list,
        verbose_name='Palabras clave de riesgo detectadas'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    
    # For future ML analysis
    emotion_scores = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Puntuaciones de emoción (ML)'
    )
    
    # Audit trail
    # history = HistoricalRecords()  # Temporarily disabled
    
    class Meta:
        verbose_name = 'Interacción de Chat'
        verbose_name_plural = 'Interacciones de Chat'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['sentiment_flag']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_risky(self):
        """Check if this interaction flagged any risks."""
        return self.sentiment_flag in ['CONCERN', 'ALERT'] or bool(self.risk_keywords_detected)


class VoiceMemo(models.Model):
    """
    Stores voice recordings from patients.
    Future: Can be transcribed and analyzed.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='voice_memos',
        verbose_name='Usuario'
    )
    
    audio_file = models.FileField(
        upload_to='voice_memos/%Y/%m/%d/',
        verbose_name='Archivo de audio'
    )
    
    transcription = models.TextField(
        blank=True,
        verbose_name='Transcripción'
    )
    
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Duración (segundos)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    # Link to chat interaction if this was part of a conversation
    related_interaction = models.ForeignKey(
        ChatInteraction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_memos',
        verbose_name='Interacción relacionada'
    )
    
    class Meta:
        verbose_name = 'Memo de Voz'
        verbose_name_plural = 'Memos de Voz'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Memo de {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
