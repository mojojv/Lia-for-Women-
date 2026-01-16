"""
Views for psychosocial module.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date

from .models import EmotionLog, CheckIn, Recommendation, ConsentRecord
from .forms import EmotionCheckInForm, RecommendationForm, ConsentForm
from .services import emotion_service, recommendation_service, consent_service
from users.decorators import patient_only, psychologist_only


@login_required
@patient_only
def emotion_checkin(request):
    """Emotion check-in form for patients."""
    if request.method == 'POST':
        form = EmotionCheckInForm(request.POST)
        if form.is_valid():
            emotion_log = form.save(commit=False)
            emotion_log.patient = request.user
            emotion_log.save()
            
            # Mark today's check-in as completed
            checkin, created = CheckIn.objects.get_or_create(
                patient=request.user,
                scheduled_date=date.today(),
                checkin_type='DAILY'
            )
            checkin.completed = True
            checkin.completion_date = timezone.now()
            checkin.related_emotion_log = emotion_log
            checkin.save()
            
            # Check if alert needed
            emotion_service.check_emotional_alert(emotion_log)
            
            messages.success(request, '¡Gracias por completar tu check-in emocional!')
            return redirect('patient:dashboard')
    else:
        form = EmotionCheckInForm()
    
    # Get recent check-ins
    recent_logs = EmotionLog.objects.filter(
        patient=request.user
    ).order_by('-timestamp')[:7]
    
    context = {
        'form': form,
        'recent_logs': recent_logs
    }
    
    return render(request, 'psychosocial/emotion_checkin.html', context)


@login_required
@patient_only
def my_recommendations(request):
    """View patient's recommendations."""
    recommendations = Recommendation.objects.filter(
        patient=request.user,
        is_active=True
    ).order_by('-created_at')
    
    # Mark recommendation as completed
    if request.method == 'POST':
        rec_id = request.POST.get('recommendation_id')
        helpful = request.POST.get('helpful') == 'yes'
        
        rec = get_object_or_404(Recommendation, id=rec_id, patient=request.user)
        rec.patient_completed = True
        rec.patient_helpful = helpful
        rec.save()
        
        messages.success(request, '¡Gracias por tu feedback!')
        return redirect('psychosocial:my_recommendations')
    
    context = {
        'recommendations': recommendations
    }
    
    return render(request, 'psychosocial/my_recommendations.html', context)


@login_required
@patient_only
def manage_consent(request):
    """Manage data sharing consent."""
    consent = consent_service.get_or_create_consent(request.user)
    
    if request.method == 'POST':
        form = ConsentForm(request.POST, instance=consent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferencias de privacidad actualizadas.')
            return redirect('users:profile')
    else:
        form = ConsentForm(instance=consent)
    
    context = {
        'form': form,
        'consent': consent
    }
    
    return render(request, 'psychosocial/manage_consent.html', context)


@login_required
@patient_only
def emotion_history(request):
    """View emotion history with charts."""
    logs = EmotionLog.objects.filter(
        patient=request.user
    ).order_by('-timestamp')[:30]
    
    # Get trend analysis
    trend = emotion_service.analyze_trend(request.user, days=7)
    averages = emotion_service.get_average_scores(request.user, days=30)
    
    context = {
        'logs': logs,
        'trend': trend,
        'averages': averages
    }
    
    return render(request, 'psychosocial/emotion_history.html', context)


@login_required
@psychologist_only
def patient_emotions(request, patient_id):
    """View patient's emotional data (psychologist-only)."""
    from users.models import CustomUser
    patient = get_object_or_404(CustomUser, id=patient_id, role='PATIENT')
    
    # Check consent
    if not consent_service.can_access_data(patient, request.user, 'emotional'):
        messages.warning(request, 'El/La paciente no ha dado consentimiento para acceder a sus datos emocionales.')
        return redirect('psychologist:dashboard')
    
    logs = EmotionLog.objects.filter(
        patient=patient
    ).order_by('-timestamp')[:30]
    
    trend = emotion_service.analyze_trend(patient, days=7)
    averages = emotion_service.get_average_scores(patient, days=30)
    adherence = recommendation_service.check_adherence(patient, days=7)
    
    context = {
        'patient': patient,
        'logs': logs,
        'trend': trend,
        'averages': averages,
        'adherence': adherence
    }
    
    return render(request, 'psychosocial/patient_emotions.html', context)


@login_required
@psychologist_only
def create_recommendation(request, patient_id):
    """Create recommendation for patient."""
    from users.models import CustomUser
    patient = get_object_or_404(CustomUser, id=patient_id, role='PATIENT')
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.patient = patient
            recommendation.created_by_psychologist = request.user
            recommendation.is_ai_generated = False
            recommendation.save()
            
            messages.success(request, 'Recomendación creada exitosamente.')
            return redirect('psychologist:dashboard')
    else:
        form = RecommendationForm()
    
    context = {
        'form': form,
        'patient': patient
    }
    
    return render(request, 'psychosocial/create_recommendation.html', context)
