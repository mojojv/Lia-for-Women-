"""
Forms for psychosocial module.
"""
from django import forms
from .models import EmotionLog, Recommendation, ConsentRecord


class EmotionCheckInForm(forms.ModelForm):
    """Form for daily/weekly emotion check-in."""
    
    class Meta:
        model = EmotionLog
        fields = ['mood_score', 'anxiety_score', 'energy_score', 'pain_emotional_impact', 'notes']
        widgets = {
            'mood_score': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'class': 'w-full mood-slider',
                'oninput': 'updateSliderValue(this, "mood")'
            }),
            'anxiety_score': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'class': 'w-full anxiety-slider',
                'oninput': 'updateSliderValue(this, "anxiety")'
            }),
            'energy_score': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'class': 'w-full energy-slider',
                'oninput': 'updateSliderValue(this, "energy")'
            }),
            'pain_emotional_impact': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'class': 'w-full pain-slider',
                'oninput': 'updateSliderValue(this, "pain")'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
                'placeholder': '¿Algo más que quieras compartir sobre cómo te sientes hoy?'
            })
        }


class RecommendationForm(forms.ModelForm):
    """Form for psychologists to create recommendations."""
    
    class Meta:
        model = Recommendation
        fields = ['recommendation_text', 'category']
        widgets = {
            'recommendation_text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
                'placeholder': 'Escribe una recomendación personalizada...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            })
        }


class ConsentForm(forms.ModelForm):
    """Form for managing patient consent."""
    
    class Meta:
        model = ConsentRecord
        fields = [
            'can_share_with_doctor',
            'can_share_chat_with_doctor',
            'can_share_with_psychologist',
            'can_use_for_research'
        ]
        widgets = {
            'can_share_with_doctor': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6 text-purple-600 rounded focus:ring-purple-500'
            }),
            'can_share_chat_with_doctor': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6 text-purple-600 rounded focus:ring-purple-500'
            }),
            'can_share_with_psychologist': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6 text-purple-600 rounded focus:ring-purple-500'
            }),
            'can_use_for_research': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6 text-purple-600 rounded focus:ring-purple-500'
            })
        }
