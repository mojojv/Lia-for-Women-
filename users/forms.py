"""
Forms for user authentication and registration.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    """Registration form for new users."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Nombre'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Apellido'
        })
    )
    
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
        })
    )
    
    phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': '+57 300 123 4567'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'nombre_usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Confirmar contraseña'
        })


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styling."""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Usuario'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
            'placeholder': 'Contraseña'
        })
    )


class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition',
                'placeholder': 'Cuéntanos un poco sobre ti...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition'
            })
        }
