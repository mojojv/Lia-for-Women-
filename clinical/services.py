"""
Services for clinical module.
Handles symptom processing and alert creation.
"""
import logging
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import SymptomReport, Alert, ClinicalTimeline

logger = logging.getLogger('clinical')


class SymptomService:
    """Service for managing symptoms."""
    
    def create_symptom_from_chat(self, patient, message, interaction):
        """
        Create symptom report from chat message.
        Extracts pain intensity if mentioned.
        """
        # Simple intensity extraction (can be enhanced with NLP)
        intensity = 5  # default
        
        # Look for numbers in message
        import re
        numbers = re.findall(r'\b([1-9]|10)\b', message)
        if numbers:
            intensity = int(numbers[0])
        
        # Determine symptom type
        symptom_type = 'PAIN'  # default
        if 'cansada' in message.lower() or 'fatigada' in message.lower():
            symptom_type = 'FATIGUE'
        elif 'náusea' in message.lower() or 'nausea' in message.lower():
            symptom_type = 'NAUSEA'
        
        symptom = SymptomReport.objects.create(
            patient=patient,
            symptom_type=symptom_type,
            intensity=intensity,
            description=message,
            reported_via='CHAT',
            related_chat=interaction
        )
        
        logger.info(f"Symptom created from chat - Patient: {patient.username}, Type: {symptom_type}")
        
        # Check if alert needed
        self.check_symptom_alerts(symptom)
        
        return symptom
    
    def check_symptom_alerts(self, symptom):
        """Check if symptom requires alert."""
        if symptom.intensity >= 8:
            alert_service.create_symptom_alert(symptom)


class AlertService:
    """Service for managing alerts."""
    
    def create_symptom_alert(self, symptom):
        """Create alert for severe symptom."""
        severity = 'CRITICAL' if symptom.intensity >= 9 else 'HIGH'
        
        alert = Alert.objects.create(
            patient=symptom.patient,
            alert_type='SYMPTOM_SEVERE',
            severity=severity,
            message=f"Síntoma severo reportado: {symptom.get_symptom_type_display()} con intensidad {symptom.intensity}/10",
            suggested_action=f"Evaluar al paciente inmediatamente. Síntoma: {symptom.get_symptom_type_display()}",
            related_symptom=symptom
        )
        
        self._send_alert_email(alert)
        
        logger.warning(f"Symptom alert created - Patient: {symptom.patient.username}, Severity: {severity}")
        
        return alert
    
    def create_chat_alert(self, patient, interaction, risk_level, suggested_action):
        """Create alert from chat risk detection."""
        severity_mapping = {
            'CRITICAL': 'CRITICAL',
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW'
        }
        
        alert = Alert.objects.create(
            patient=patient,
            alert_type='CHAT_RISK',
            severity=severity_mapping.get(risk_level, 'MEDIUM'),
            message=f"Riesgo {risk_level} detectado en conversación con Lia",
            suggested_action=suggested_action or "Revisar conversación y contactar al paciente",
            related_chat=interaction
        )
        
        if risk_level in ['CRITICAL', 'HIGH']:
            self._send_alert_email(alert)
        
        logger.warning(f"Chat alert created - Patient: {patient.username}, Risk: {risk_level}")
        
        return alert
    
    def resolve_alert(self, alert, resolved_by, notes):
        """Mark alert as resolved."""
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = resolved_by
        alert.resolution_notes = notes
        alert.save()
        
        logger.info(f"Alert resolved - ID: {alert.id}, By: {resolved_by.username}")
    
    def _send_alert_email(self, alert):
        """Send email notification for alert."""
        try:
            # Get assigned doctor
            doctor = alert.patient.profile.assigned_doctor
            if not doctor or not doctor.email:
                logger.warning(f"No doctor assigned or no email for patient {alert.patient.username}")
                return
            
            subject = f"⚠ Alerta {alert.get_severity_display()} - {alert.patient.get_full_name()}"
            message = f"""
Alerta: {alert.get_alert_type_display()}
Paciente: {alert.patient.get_full_name()}
Severidad: {alert.get_severity_display()}

Mensaje:
{alert.message}

Acción sugerida:
{alert.suggested_action}

---
Sistema Lia for a Woman
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [doctor.email],
                fail_silently=False,
            )
            
            alert.email_sent = True
            alert.save()
            
            logger.info(f"Alert email sent to {doctor.email}")
            
        except Exception as e:
            logger.error(f"Error sending alert email: {str(e)}")


class TimelineService:
    """Service for managing clinical timeline."""
    
    def add_event(self, patient, event_type, description, event_date, created_by=None):
        """Add event to clinical timeline."""
        event = ClinicalTimeline.objects.create(
            patient=patient,
            event_type=event_type,
            event_description=description,
            event_date=event_date,
            created_by=created_by
        )
        
        logger.info(f"Timeline event added - Patient: {patient.username}, Type: {event_type}")
        
        return event


# Singleton instances
symptom_service = SymptomService()
alert_service = AlertService()
timeline_service = TimelineService()
