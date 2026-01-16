"""
Views for patient dashboard.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from users.decorators import patient_only
from clinical.models import SymptomReport, Alert
from psychosocial.models import EmotionLog, Recommendation, CheckIn
from chatbot.models import ChatInteraction


@login_required
@patient_only
def dashboard(request):
    """
    Main patient dashboard.
    Shows wellness indicator, quick actions, and recent activity.
    """
    patient = request.user
    
    # Get recent data
    recent_symptoms = SymptomReport.objects.filter(
        patient=patient
    ).order_by('-timestamp')[:5]
    
    recent_emotions = EmotionLog.objects.filter(
        patient=patient
    ).order_by('-timestamp')[:5]
    
    active_recommendations = Recommendation.objects.filter(
        patient=patient,
        is_active=True,
        patient_completed=False
    ).order_by('-created_at')[:3]
    
    recent_chats = ChatInteraction.objects.filter(
        user=patient
    ).order_by('-timestamp')[:3]
    
    # Wellness indicator (traffic light)
    wellness_status = _calculate_wellness_status(patient)
    
    # Check if today's check-in is done
    today_checkin = CheckIn.objects.filter(
        patient=patient,
        scheduled_date=date.today(),
        checkin_type='DAILY'
    ).first()
    
    checkin_completed = today_checkin and today_checkin.completed if today_checkin else False
    
    context = {
        'patient': patient,
        'wellness_status': wellness_status,
        'recent_symptoms': recent_symptoms,
        'recent_emotions': recent_emotions,
        'active_recommendations': active_recommendations,
        'recent_chats': recent_chats,
        'checkin_completed': checkin_completed,
    }
    
    return render(request, 'patient/dashboard.html', context)


def _calculate_wellness_status(patient):
    """
    Calculate overall wellness status: GREEN, YELLOW, or RED.
    """
    # Get most recent emotion log
    recent_emotion = EmotionLog.objects.filter(
        patient=patient
    ).order_by('-timestamp').first()
    
    # Get recent severe symptoms
    severe_symptoms = SymptomReport.objects.filter(
        patient=patient,
        intensity__gte=8,
        timestamp__gte=date.today() - timedelta(days=3)
    ).count()
    
    # Get unresolved alerts
    active_alerts = Alert.objects.filter(
        patient=patient,
        is_resolved=False,
        severity__in=['HIGH', 'CRITICAL']
    ).count()
    
    # Determine status
    if active_alerts > 0 or severe_symptoms > 0:
        return 'RED'
    elif recent_emotion and recent_emotion.needs_attention:
        return 'YELLOW'
    elif recent_emotion and recent_emotion.overall_wellbeing >= 6:
        return 'GREEN'
    else:
        return 'YELLOW'
