"""
Views for doctor dashboard.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date, timedelta

from users.decorators import doctor_only
from users.models import CustomUser
from clinical.models import SymptomReport, Alert, ClinicalTimeline
from psychosocial.services import consent_service


@login_required
@doctor_only
def dashboard(request):
    """
    Doctor dashboard showing assigned patients with alert indicators.
    """
    doctor = request.user
    
    # Get assigned patients
    assigned_patients = CustomUser.objects.filter(
        profile__assigned_doctor=doctor,
        role='PATIENT'
    ).annotate(
        active_alerts_count=Count(
            'alerts',
            filter=Q(alerts__is_resolved=False)
        ),
        critical_alerts_count=Count(
            'alerts',
            filter=Q(alerts__is_resolved=False, alerts__severity='CRITICAL')
        ),
        high_alerts_count=Count(
            'alerts',
            filter=Q(alerts__is_resolved=False, alerts__severity='HIGH')
        )
    ).order_by('-critical_alerts_count', '-high_alerts_count')
    
    # Recent alerts across all patients
    recent_alerts = Alert.objects.filter(
        patient__profile__assigned_doctor=doctor,
        is_resolved=False
    ).order_by('-severity', '-created_at')[:10]
    
    # Statistics
    total_patients = assigned_patients.count()
    patients_with_alerts = assigned_patients.filter(active_alerts_count__gt=0).count()
    critical_alerts = Alert.objects.filter(
        patient__profile__assigned_doctor=doctor,
        is_resolved=False,
        severity='CRITICAL'
    ).count()
    
    context = {
        'doctor': doctor,
        'assigned_patients': assigned_patients,
        'recent_alerts': recent_alerts,
        'total_patients': total_patients,
        'patients_with_alerts': patients_with_alerts,
        'critical_alerts': critical_alerts,
    }
    
    return render(request, 'doctor/dashboard.html', context)


@login_required
@doctor_only
def patient_detail(request, patient_id):
    """
    Detailed view of a specific patient.
    Tabs for clinical data, alerts, timeline.
    """
    doctor = request.user
    patient = get_object_or_404(
        CustomUser,
        id=patient_id,
        role='PATIENT',
        profile__assigned_doctor=doctor
    )
    
    # Check if doctor can access chat
    can_access_chat = consent_service.can_access_data(patient, doctor, 'chat')
    
    # Get clinical data
    recent_symptoms = SymptomReport.objects.filter(
        patient=patient
    ).order_by('-timestamp')[:20]
    
    active_alerts = Alert.objects.filter(
        patient=patient,
        is_resolved=False
    ).order_by('-severity', '-created_at')
    
    timeline_events = ClinicalTimeline.objects.filter(
        patient=patient
    ).order_by('-event_date')[:15]
    
    # Statistics
    avg_symptom_intensity = SymptomReport.objects.filter(
        patient=patient,
        timestamp__gte=date.today() - timedelta(days=7)
    ).aggregate(
        avg_intensity=models.Avg('intensity')
    )['avg_intensity']
    
    context = {
        'patient': patient,
        'can_access_chat': can_access_chat,
        'recent_symptoms': recent_symptoms,
        'active_alerts': active_alerts,
        'timeline_events': timeline_events,
        'avg_symptom_intensity': avg_symptom_intensity or 0,
    }
    
    return render(request, 'doctor/patient_detail.html', context)


from django.db import models  # Import needed for aggregate
