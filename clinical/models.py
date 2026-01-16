"""
Models for clinical module.
Tracks symptoms, alerts, and clinical timeline.
"""
from django.db import models
from django.conf import settings
# # from simple_history.models import HistoricalRecords  # Temporarily disabled  # Temporarily disabled


class SymptomReport(models.Model):
    """
    Patient-reported symptoms.
    Can be created via chat or manual form.
    """
    SYMPTOM_TYPE_CHOICES = [
        ('PAIN', 'Dolor'),
        ('FATIGUE', 'Fatiga'),
        ('NAUSEA', 'Náusea'),
        ('VOMITING', 'Vómito'),
        ('FEVER', 'Fiebre'),
        ('INSOMNIA', 'Insomnio'),
        ('APPETITE_LOSS', 'Pérdida de apetito'),
        ('OTHER', 'Otro'),
    ]
    
    REPORTED_VIA_CHOICES = [
        ('CHAT', 'Chat con Lia'),
        ('FORM', 'Formulario'),
        ('VOICE', 'Memo de voz'),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='symptom_reports',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    symptom_type = models.CharField(
        max_length=20,
        choices=SYMPTOM_TYPE_CHOICES,
        verbose_name='Tipo de síntoma'
    )
    
    intensity = models.IntegerField(
        help_text='Intensidad de 1 a 10',
        verbose_name='Intensidad'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text='Para dolor: ubicación del dolor',
        verbose_name='Ubicación'
    )
    
    reported_via = models.CharField(
        max_length=10,
        choices=REPORTED_VIA_CHOICES,
        default='FORM',
        verbose_name='Reportado vía'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    
    # Link to chat interaction if from chat
    related_chat = models.ForeignKey(
        'chatbot.ChatInteraction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Interacción de chat relacionada'
    )
    
    # Doctor notes
    doctor_notes = models.TextField(
        blank=True,
        verbose_name='Notas del médico'
    )
    
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_symptoms',
        limit_choices_to={'role': 'DOCTOR'},
        verbose_name='Revisado por'
    )
    
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de revisión'
    )
    
    # Audit trail
    # history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Reporte de Síntoma'
        verbose_name_plural = 'Reportes de Síntomas'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['patient', '-timestamp']),
            models.Index(fields=['symptom_type', 'intensity']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.get_symptom_type_display()} ({self.intensity}/10)"
    
    @property
    def is_severe(self):
        """Check if symptom is severe (intensity >= 8)."""
        return self.intensity >= 8


class Alert(models.Model):
    """
    System-generated alerts for medical team.
    Created automatically based on rules.
    """
    ALERT_TYPE_CHOICES = [
        ('SYMPTOM_SEVERE', 'Síntoma Severo'),
        ('EMOTION_CRISIS', 'Crisis Emocional'),
        ('MISSED_CHECKIN', 'Check-in Perdido'),
        ('CHAT_RISK', 'Riesgo Detectado en Chat'),
        ('MANUAL', 'Manual'),
    ]
    
    SEVERITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alerts',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPE_CHOICES,
        verbose_name='Tipo de alerta'
    )
    
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        verbose_name='Severidad'
    )
    
    message = models.TextField(
        verbose_name='Mensaje'
    )
    
    suggested_action = models.TextField(
        blank=True,
        verbose_name='Acción sugerida'
    )
    
    is_resolved = models.BooleanField(
        default=False,
        verbose_name='Resuelta'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de resolución'
    )
    
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts',
        verbose_name='Resuelta por'
    )
    
    resolution_notes = models.TextField(
        blank=True,
        verbose_name='Notas de resolución'
    )
    
    # Related objects
    related_symptom = models.ForeignKey(
        SymptomReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Síntoma relacionado'
    )
    
    related_chat = models.ForeignKey(
        'chatbot.ChatInteraction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Chat relacionado'
    )
    
    # Email notification sent
    email_sent = models.BooleanField(
        default=False,
        verbose_name='Email enviado'
    )
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', 'is_resolved', '-created_at']),
            models.Index(fields=['severity', 'is_resolved']),
        ]
    
    def __str__(self):
        status = "✓" if self.is_resolved else "⚠"
        return f"{status} {self.patient.username} - {self.get_alert_type_display()} ({self.get_severity_display()})"


class ClinicalTimeline(models.Model):
    """
    Timeline of clinical events.
    Auto-generated and manual entries.
    """
    EVENT_TYPE_CHOICES = [
        ('DIAGNOSIS', 'Diagnóstico'),
        ('TREATMENT', 'Tratamiento'),
        ('SURGERY', 'Cirugía'),
        ('SYMPTOM', 'Síntoma'),
        ('APPOINTMENT', 'Cita Médica'),
        ('LAB_RESULT', 'Resultado de Laboratorio'),
        ('OTHER', 'Otro'),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clinical_timeline',
        limit_choices_to={'role': 'PATIENT'},
        verbose_name='Paciente'
    )
    
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        verbose_name='Tipo de evento'
    )
    
    event_description = models.TextField(
        verbose_name='Descripción del evento'
    )
    
    event_date = models.DateField(
        verbose_name='Fecha del evento'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_timeline_events',
        verbose_name='Creado por'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    
    # Audit trail
    # history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Evento de Línea de Tiempo'
        verbose_name_plural = 'Eventos de Línea de Tiempo'
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.patient.username} - {self.get_event_type_display()} ({self.event_date})"
