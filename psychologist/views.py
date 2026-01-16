"""
Views for psychologist dashboard.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from datetime import date, timedelta

from users.decorators import psychologist_only
from users.models import CustomUser
from psychosocial.models import EmotionLog, Recommendation, CheckIn
from psychosocial.services import emotion_service, consent_service


@login_required
@psychologist_only
def dashboard(request):
    """
    Psychologist dashboard showing assigned patients with emotional metrics.
    """
    psychologist = request.user
    
    # Get assigned patients
    assigned_patients = CustomUser.objects.filter(
        profile__assigned_psychologist=psychologist,
        role='PATIENT'
    )
    
    # Prepare patient data with metrics
    patient_data = []
    for patient in assigned_patients:
        # Check consent
        can_access = consent_service.can_access_data(patient, psychologist, 'emotional')
        
        if can_access:
            # Get recent averages
            recent_logs = EmotionLog.objects.filter(
                patient=patient,
                timestamp__gte=date.today() - timedelta(days=7)
            )
            
            avg_scores = recent_logs.aggregate(
                avg_mood=Avg('mood_score'),
                avg_anxiety=Avg('anxiety_score'),
                avg_energy=Avg('energy_score')
            )
            
            trend = emotion_service.analyze_trend(patient, days=7)
            
            patient_data.append({
                'patient': patient,
                'avg_mood': avg_scores['avg_mood'] or 0,
                'avg_anxiety': avg_scores['avg_anxiety'] or 0,
                'avg_energy': avg_scores['avg_energy'] or 0,
                'trend': trend,
                'can_access': True
            })
        else:
            patient_data.append({
                'patient': patient,
                'can_access': False
            })
    
    # Statistics
    total_patients = assigned_patients.count()
    patients_with_access = sum(1 for p in patient_data if p.get('can_access'))
    patients_declining = sum(1 for p in patient_data if p.get('trend') == 'DECLINING')
    
    context = {
        'psychologist': psychologist,
        'patient_data': patient_data,
        'total_patients': total_patients,
        'patients_with_access': patients_with_access,
        'patients_declining': patients_declining,
    }
    
    return render(request, 'psychologist/dashboard.html', context)


@login_required
@psychologist_only
def patient_emotional_detail(request, patient_id):
    """
    Detailed emotional view of a specific patient.
    Shows charts and trends.
    """
    psychologist = request.user
    patient = get_object_or_404(
        CustomUser,
        id=patient_id,
        role='PATIENT',
        profile__assigned_psychologist=psychologist
    )
    
    # Check consent
    if not consent_service.can_access_data(patient, psychologist, 'emotional'):
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.warning(request, 'El/La paciente no ha dado consentimiento.')
        return redirect('psychologist:dashboard')
    
    # Get emotion logs for charts
    emotion_logs = EmotionLog.objects.filter(
        patient=patient
    ).order_by('-timestamp')[:30]
    
    # Get trend
    trend = emotion_service.analyze_trend(patient, days=7)
    trend_30 = emotion_service.analyze_trend(patient, days=30)
    
    # Get recommendations
    patient_recommendations = Recommendation.objects.filter(
        patient=patient
    ).order_by('-created_at')[:10]
    
    # Adherence
    from psychosocial.services import recommendation_service
    adherence = recommendation_service.check_adherence(patient, days=7)
    
    context = {
        'patient': patient,
        'emotion_logs': emotion_logs,
        'trend_7day': trend,
        'trend_30day': trend_30,
        'patient_recommendations': patient_recommendations,
        'adherence': adherence,
    }
    
    return render(request, 'psychologist/patient_detail.html', context)
