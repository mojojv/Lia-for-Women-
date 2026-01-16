"""
User models for Lia for a Woman system.
Implements custom user with role-based access control.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
# from simple_history.models import HistoricalRecords  # Temporarily disabled


class CustomUser(AbstractUser):
    """
    Custom user model with role-based access.
    Extends Django's AbstractUser with additional fields for the Lia system.
    """
    ROLE_CHOICES = [
        ('PATIENT', 'Paciente'),
        ('DOCTOR', 'Médico'),
        ('PSYCHOLOGIST', 'Psicólogo/a'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='PATIENT',
        verbose_name='Rol'
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name='Teléfono'
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verificado'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    # history = HistoricalRecords()  # Temporarily disabled
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_patient(self):
        return self.role == 'PATIENT'
    
    def is_doctor(self):
        return self.role == 'DOCTOR'
    
    def is_psychologist(self):
        return self.role == 'PSYCHOLOGIST'


class Profile(models.Model):
    """
    Extended profile information for users.
    OneToOne relationship with CustomUser.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de nacimiento'
    )
    
    medical_record_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Número de historia clínica'
    )
    
    # For patients: assigned healthcare team
    assigned_doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_as_doctor',
        limit_choices_to={'role': 'DOCTOR'},
        verbose_name='Médico asignado'
    )
    
    assigned_psychologist = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_as_psychologist',
        limit_choices_to={'role': 'PSYCHOLOGIST'},
        verbose_name='Psicólogo/a asignado/a'
    )
    
    bio = models.TextField(
        blank=True,
        verbose_name='Biografía'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Foto de perfil'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    # history = HistoricalRecords()  # Temporarily disabled
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def age(self):
        """Calculate age from birth date."""
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
