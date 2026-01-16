"""
Models for psychosocial module.
Tracks emotional state, check-ins, recommendations, and consent.
"""
from django.db import models
from django.conf import settings
# from simple_history.models import HistoricalRecords  # Temporarily disabled


class EmotionLog(models.Model):
    """
    Daily/weekly emotion tracking.
    Uses Likert scales for different emotional dimensions.
    """
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emotion_logs',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    # Likert scales (1-10)
    mood_score = models.IntegerField(
        help_text='Estado de ánimo general (1=Muy mal, 10=Excelente)',
        verbose_name='Estado de ánimo'
    )
    
    anxiety_score = models.IntegerField(
        help_text='Nivel de ansiedad (1=Sin ansiedad, 10=Ansiedad extrema)',
        verbose_name='Nivel de ansiedad'
    )
    
    energy_score = models.IntegerField(
        help_text='Nivel de energía (1=Agotado/a, 10=Muy energizado/a)',
        verbose_name='Nivel de energía'
    )
    
    pain_emotional_impact = models.IntegerField(
        null=True,
        blank=True,
        help_text='Impacto emocional del dolor (1=Bajo, 10=Alto)',
        verbose_name='Impacto emocional del dolor'
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name='Notas adicionales'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    
    # Audit trail
    # history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Registro Emocional'
        verbose_name_plural = 'Registros Emocionales'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['patient', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.timestamp.strftime('%Y-%m-%d')}"
    
    @property
    def overall_wellbeing(self):
        """Calculate overall wellbeing score (average)."""
        scores = [self.mood_score, self.energy_score]
        # Invert anxiety (higher anxiety = lower wellbeing)
        inverted_anxiety = 11 - self.anxiety_score
        scores.append(inverted_anxiety)
        return sum(scores) / len(scores)
    
    @property
    def needs_attention(self):
        """Check if emotional state needs attention."""
        return (
            self.mood_score <= 3 or
            self.anxiety_score >= 8 or
            self.energy_score <= 2
        )


class CheckIn(models.Model):
    """
    Tracks completion of emotional check-ins.
    Helps monitor adherence.
    """
    CHECKIN_TYPE_CHOICES = [
        ('DAILY', 'Diario'),
        ('WEEKLY', 'Semanal'),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='checkins',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    checkin_type = models.CharField(
        max_length=10,
        choices=CHECKIN_TYPE_CHOICES,
        default='DAILY',
        verbose_name='Tipo de check-in'
    )
    
    scheduled_date = models.DateField(
        verbose_name='Fecha programada'
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name='Completado'
    )
    
    completion_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de completado'
    )
    
    # Link to emotion log if completed
    related_emotion_log = models.OneToOneField(
        EmotionLog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Registro emocional relacionado'
    )
    
    class Meta:
        verbose_name = 'Check-in'
        verbose_name_plural = 'Check-ins'
        ordering = ['-scheduled_date']
        unique_together = ['patient', 'scheduled_date', 'checkin_type']
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.patient.username} - {self.scheduled_date}"


class Recommendation(models.Model):
    """
    Personalized recommendations for patients.
    Can be AI-generated or created by psychologists.
    """
    CATEGORY_CHOICES = [
        ('EXERCISE', 'Ejercicio'),
        ('MEDITATION', 'Meditación'),
        ('SOCIAL', 'Actividad Social'),
        ('READING', 'Lectura'),
        ('HOBBY', 'Hobby'),
        ('NUTRITION', 'Nutrición'),
        ('SLEEP', 'Sueño'),
        ('OTHER', 'Otro'),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    recommendation_text = models.TextField(
        verbose_name='Recomendación'
    )
    
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        verbose_name='Categoría'
    )
    
    is_ai_generated = models.BooleanField(
        default=False,
        verbose_name='Generado por IA'
    )
    
    created_by_psychologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_recommendations',
        limit_choices_to={'role': 'PSYCHOLOGIST'},
        verbose_name='Creado por psicólogo/a'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    
    # Patient feedback
    patient_completed = models.BooleanField(
        default=False,
        verbose_name='Completada por paciente'
    )
    
    patient_helpful = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='Fue útil'
    )
    
    class Meta:
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        source = "IA" if self.is_ai_generated else "Psicólogo/a"
        return f"{self.patient.username} - {self.get_category_display()} ({source})"


class ConsentRecord(models.Model):
    """
    Patient consent for data sharing.
    GDPR-like compliance.
    """
    patient = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consent_record',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    can_share_with_doctor = models.BooleanField(
        default=True,
        verbose_name='Compartir datos clínicos con médico'
    )
    
    can_share_chat_with_doctor = models.BooleanField(
        default=False,
        verbose_name='Compartir conversaciones de chat con médico'
    )
    
    can_share_with_psychologist = models.BooleanField(
        default=True,
        verbose_name='Compartir datos emocionales con psicólogo/a'
    )
    
    can_use_for_research = models.BooleanField(
        default=False,
        verbose_name='Uso de datos para investigación (anonimizados)'
    )
    
    consent_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de consentimiento'
    )
    
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    # Audit trail
    # history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Registro de Consentimiento'
        verbose_name_plural = 'Registros de Consentimiento'
    
    def __str__(self):
        return f"Consentimiento de {self.patient.username}"
