"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    """Admin interface for CustomUser."""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'phone', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'email', 'first_name', 'last_name', 'phone')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin):
    """Admin interface for Profile."""
    
    list_display = ('user', 'birth_date', 'assigned_doctor', 'assigned_psychologist')
    search_fields = ('user__username', 'user__email', 'medical_record_number')
    list_filter = ('assigned_doctor', 'assigned_psychologist')
    
    autocomplete_fields = ['user', 'assigned_doctor', 'assigned_psychologist']
