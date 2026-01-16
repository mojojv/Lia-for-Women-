"""
Forms for clinical module.
"""
from django import forms
from .models import SymptomReport, ClinicalTimeline


class SymptomReportForm(forms.ModelForm):
    """Form for reporting symptoms."""
    
    class Meta:
        model = SymptomReport
        fields = ['symptom_type', 'intensity', 'description', 'location']
        widgets = {
            'symptom_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            }),
            'intensity': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'class': 'w-full',
                'oninput': 'this.nextElementSibling.value = this.value'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
                'placeholder': 'Describe cómo te sientes...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
                'placeholder': 'Ej: Cabeza, Estómago, Pecho'
            })
        }


class TimelineEventForm(forms.ModelForm):
    """Form for adding timeline events (doctor-only)."""
    
    class Meta:
        model = ClinicalTimeline
        fields = ['event_type', 'event_description', 'event_date']
        widgets = {
            'event_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            }),
            'event_description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            }),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            })
        }
