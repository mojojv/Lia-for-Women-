"""
Services for psychosocial module.
Handles emotion analysis and recommendation generation.
"""
import logging
from datetime import date, timedelta
from django.db.models import Avg

from .models import EmotionLog, CheckIn, Recommendation, ConsentRecord

logger = logging.getLogger('psychosocial')


class EmotionService:
    """Service for analyzing emotional trends."""
    
    def analyze_trend(self, patient, days=7):
        """
        Analyze emotion trend over specified days.
        Returns: IMPROVING, STABLE, or DECLINING
        """
        logs = EmotionLog.objects.filter(
            patient=patient,
            timestamp__gte=date.today() - timedelta(days=days)
        ).order_by('timestamp')
        
        if logs.count() < 2:
            return 'INSUFFICIENT_DATA'
        
        # Get first and last wellbeing scores
        first_score = logs.first().overall_wellbeing
        last_score = logs.last().overall_wellbeing
        
        # Calculate trend
        difference = last_score - first_score
        
        if difference > 1:
            return 'IMPROVING'
        elif difference < -1:
            return 'DECLINING'
        else:
            return 'STABLE'
    
    def get_average_scores(self, patient, days=30):
        """Get average emotional scores over period."""
        logs = EmotionLog.objects.filter(
            patient=patient,
            timestamp__gte=date.today() - timedelta(days=days)
        )
        
        averages = logs.aggregate(
            avg_mood=Avg('mood_score'),
            avg_anxiety=Avg('anxiety_score'),
            avg_energy=Avg('energy_score')
        )
        
        return averages
    
    def check_emotional_alert(self, emotion_log):
        """Check if emotion log requires alert."""
        if emotion_log.needs_attention:
            from clinical.services import alert_service
            
            # Create emotional crisis alert
            from clinical.models import Alert
            
            alert = Alert.objects.create(
                patient=emotion_log.patient,
                alert_type='EMOTION_CRISIS',
                severity='MEDIUM' if emotion_log.mood_score <= 3 else 'LOW',
                message=f"Estado emocional preocupante detectado. Ánimo: {emotion_log.mood_score}/10, Ansiedad: {emotion_log.anxiety_score}/10",
                suggested_action="Contactar al paciente para seguimiento psicológico."
            )
            
            logger.warning(f"Emotional alert created for {emotion_log.patient.username}")
            
            return alert
        
        return None


class RecommendationService:
    """Service for generating personalized recommendations."""
    
    # Rule-based recommendation templates
    RECOMMENDATIONS = {
        'LOW_MOOD': [
            "Considera dar un paseo corto al aire libre. La naturaleza puede ayudar a mejorar el ánimo.",
            "Prueba escuchar música que te guste. La música puede tener un efecto positivo en el estado de ánimo.",
            "Conecta con un ser querido, aunque sea por mensaje. El apoyo social es invaluable.",
        ],
        'HIGH_ANXIETY': [
            "Intenta una técnica de respiración: inhala por 4, mantén por 4, exhala por 6.",
            "Prueba la meditación guiada. Hay apps gratuitas que pueden ayudarte.",
            "Escribe tus preocupaciones en un diario. A veces expresarlas ayuda a procesarlas.",
        ],
        'LOW_ENERGY': [
            "Asegúrate de estar hidratándote bien. La deshidratación puede causar fatiga.",
            "Intenta una siesta corta de 20 minutos. Puede ayudar a restaurar energía.",
            "Considera alimentos nutritivos y ligeros que te den energía sin pesadez.",
        ],
        'GENERAL': [
            "Mantén una rutina de sueño regular. Dormir bien es fundamental para el bienestar.",
            "Practica la gratitud: escribe 3 cosas por las que estés agradecida hoy.",
            "Haz algo pequeño que disfrutes cada día, aunque sea 10 minutos.",
        ]
    }
    
    def generate_recommendation_for_patient(self, patient):
        """
        Generate AI recommendation based on recent emotional state.
        """
        import random
        
        # Get recent emotion logs
        recent_logs = EmotionLog.objects.filter(
            patient=patient
        ).order_by('-timestamp')[:7]
        
        if not recent_logs:
            category = 'GENERAL'
            recommendations = self.RECOMMENDATIONS['GENERAL']
        else:
            # Analyze patterns
            avg_mood = sum(log.mood_score for log in recent_logs) / len(recent_logs)
            avg_anxiety = sum(log.anxiety_score for log in recent_logs) / len(recent_logs)
            avg_energy = sum(log.energy_score for log in recent_logs) / len(recent_logs)
            
            # Determine category
            if avg_mood <= 4:
                category = 'MEDITATION'
                recommendations = self.RECOMMENDATIONS['LOW_MOOD']
            elif avg_anxiety >= 7:
                category = 'MEDITATION'
                recommendations = self.RECOMMENDATIONS['HIGH_ANXIETY']
            elif avg_energy <= 4:
                category = 'EXERCISE'
                recommendations = self.RECOMMENDATIONS['LOW_ENERGY']
            else:
                category = 'OTHER'
                recommendations = self.RECOMMENDATIONS['GENERAL']
        
        # Create recommendation
        recommendation = Recommendation.objects.create(
            patient=patient,
            recommendation_text=random.choice(recommendations),
            category=category,
            is_ai_generated=True
        )
        
        logger.info(f"AI recommendation generated for {patient.username}")
        
        return recommendation
    
    def check_adherence(self, patient, days=7):
        """
        Check check-in adherence over period.
        Returns completion rate (0-1).
        """
        checkins = CheckIn.objects.filter(
            patient=patient,
            scheduled_date__gte=date.today() - timedelta(days=days)
        )
        
        if checkins.count() == 0:
            return None
        
        completed = checkins.filter(completed=True).count()
        total = checkins.count()
        
        return completed / total


class ConsentService:
    """Service for managing patient consent."""
    
    def get_or_create_consent(self, patient):
        """Get or create consent record for patient."""
        consent, created = ConsentRecord.objects.get_or_create(
            patient=patient
        )
        
        if created:
            logger.info(f"Consent record created for {patient.username}")
        
        return consent
    
    def can_access_data(self, patient, requester, data_type='clinical'):
        """
        Check if requester can access patient data.
        
        Args:
            patient: Patient whose data is being accessed
            requester: User requesting access
            data_type: 'clinical', 'chat', or 'emotional'
        """
        # Patient can always access their own data
        if patient == requester:
            return True
        
        # Get consent
        try:
            consent = ConsentRecord.objects.get(patient=patient)
        except ConsentRecord.DoesNotExist:
            # No consent record = default to False for safety
            return False
        
        # Check based on data type and requester role
        if requester.role == 'DOCTOR':
            if data_type == 'clinical':
                return consent.can_share_with_doctor
            elif data_type == 'chat':
                return consent.can_share_chat_with_doctor
            else:
                return False
        
        elif requester.role == 'PSYCHOLOGIST':
            if data_type == 'emotional':
                return consent.can_share_with_psychologist
            else:
                return False
        
        return False


# Singleton instances
emotion_service = EmotionService()
recommendation_service = RecommendationService()
consent_service = ConsentService()
