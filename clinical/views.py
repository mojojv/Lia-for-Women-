"""
Views for clinical module.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import SymptomReport, Alert, ClinicalTimeline
from .forms import SymptomReportForm, TimelineEventForm
from .services import symptom_service, alert_service, timeline_service
from users.decorators import patient_only, doctor_only


@login_required
@patient_only
def report_symptom(request):
    """Patient form to report symptoms."""
    if request.method == 'POST':
        form = SymptomReportForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.patient = request.user
            symptom.reported_via = 'FORM'
            symptom.save()
            
            # Check for alerts
            symptom_service.check_symptom_alerts(symptom)
            
            messages.success(request, 'Síntoma registrado exitosamente.')
            return redirect('patient:dashboard')
    else:
        form = SymptomReportForm()
    
    return render(request, 'clinical/report_symptom.html', {'form': form})


@login_required
@patient_only
def my_symptoms(request):
    """View patient's own symptom history."""
    symptoms = SymptomReport.objects.filter(
        patient=request.user
    ).order_by('-timestamp')
    
    return render(request, 'clinical/my_symptoms.html', {'symptoms': symptoms})


@login_required
@doctor_only
def patient_symptoms(request, patient_id):
    """View symptoms for a specific patient (doctor-only)."""
    from users.models import CustomUser
    patient = get_object_or_404(CustomUser, id=patient_id, role='PATIENT')
    
    symptoms = SymptomReport.objects.filter(
        patient=patient
    ).order_by('-timestamp')
    
    context = {
        'patient': patient,
        'symptoms': symptoms
    }
    
    return render(request, 'clinical/patient_symptoms.html', context)


@login_required
@doctor_only
def patient_timeline(request, patient_id):
    """View clinical timeline for patient."""
    from users.models import CustomUser
    patient = get_object_or_404(CustomUser, id=patient_id, role='PATIENT')
    
    timeline_events = ClinicalTimeline.objects.filter(
        patient=patient
    ).order_by('-event_date')
    
    if request.method == 'POST':
        form = TimelineEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.patient = patient
            event.created_by = request.user
            event.save()
            
            messages.success(request, 'Evento agregado a la línea de tiempo.')
            return redirect('clinical:patient_timeline', patient_id=patient_id)
    else:
        form = TimelineEventForm()
    
    context = {
        'patient': patient,
        'timeline_events': timeline_events,
        'form': form
    }
    
    return render(request, 'clinical/patient_timeline.html', context)


@login_required
@doctor_only
def resolve_alert(request, alert_id):
    """Resolve an alert."""
    alert = get_object_or_404(Alert, id=alert_id)
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        alert_service.resolve_alert(alert, request.user, notes)
        
        messages.success(request, 'Alerta resuelta exitosamente.')
        return redirect('doctor:dashboard')
    
    return render(request, 'clinical/resolve_alert.html', {'alert': alert})
