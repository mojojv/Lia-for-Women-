"""
Admin configuration for clinical app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import SymptomReport, Alert, ClinicalTimeline


@admin.register(SymptomReport)
class SymptomReportAdmin(SimpleHistoryAdmin):
    """Admin for symptom reports."""
    
    list_display = ('patient', 'symptom_type', 'intensity', 'timestamp', 'is_severe', 'reviewed_by')
    list_filter = ('symptom_type', 'intensity', 'reported_via', 'timestamp')
    search_fields = ('patient__username', 'description')
    readonly_fields = ('timestamp',)
    
    def is_severe(self, obj):
        return obj.is_severe
    is_severe.boolean = True


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """Admin for alerts."""
    
    list_display = ('patient', 'alert_type', 'severity', 'created_at', 'is_resolved', 'email_sent')
    list_filter = ('alert_type', 'severity', 'is_resolved', 'created_at')
    search_fields = ('patient__username', 'message')
    readonly_fields = ('created_at',)


@admin.register(ClinicalTimeline)
class ClinicalTimelineAdmin(SimpleHistoryAdmin):
    """Admin for clinical timeline."""
    
    list_display = ('patient', 'event_type', 'event_date', 'created_by')
    list_filter = ('event_type', 'event_date')
    search_fields = ('patient__username', 'event_description')
