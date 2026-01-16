"""
Custom decorators for role-based access control.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """
    Decorator to restrict access based on user role.
    
    Usage:
        @role_required('PATIENT')
        @role_required('DOCTOR', 'PSYCHOLOGIST')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder.')
                return redirect('users:login')
            
            if request.user.role not in roles:
                messages.error(
                    request,
                    'No tienes permisos para acceder a esta página.'
                )
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def patient_only(view_func):
    """Shortcut decorator for patient-only views."""
    return role_required('PATIENT')(view_func)


def doctor_only(view_func):
    """Shortcut decorator for doctor-only views."""
    return role_required('DOCTOR')(view_func)


def psychologist_only(view_func):
    """Shortcut decorator for psychologist-only views."""
    return role_required('PSYCHOLOGIST')(view_func)


def medical_staff_only(view_func):
    """Decorator for doctor and psychologist access."""
    return role_required('DOCTOR', 'PSYCHOLOGIST')(view_func)


def patient_consent_required(consent_field):
    """
    Decorator to check if patient has given consent for data access.
    
    Usage:
        @patient_consent_required('can_share_with_doctor')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get patient_id from URL kwargs or request
            patient_id = kwargs.get('patient_id')
            
            if not patient_id:
                messages.error(request, 'ID de paciente no proporcionado.')
                return redirect('users:dashboard_redirect')
            
            # Check consent
            from psychosocial.models import ConsentRecord
            try:
                consent = ConsentRecord.objects.get(patient_id=patient_id)
                
                # Check specific consent field
                if not getattr(consent, consent_field, False):
                    messages.warning(
                        request,
                        'El/La paciente no ha dado consentimiento para acceder a esta información.'
                    )
                    return redirect('users:dashboard_redirect')
                    
            except ConsentRecord.DoesNotExist:
                messages.warning(
                    request,
                    'No se ha registrado el consentimiento del/la paciente.'
                )
                return redirect('users:dashboard_redirect')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
