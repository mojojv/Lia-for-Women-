"""
Admin configuration for psychosocial app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import EmotionLog, CheckIn, Recommendation, ConsentRecord


@admin.register(EmotionLog)
class EmotionLogAdmin(SimpleHistoryAdmin):
    """Admin for emotion logs."""
    
    list_display = ('patient', 'timestamp', 'mood_score', 'anxiety_score', 'energy_score', 'needs_attention')
    list_filter = ('timestamp', 'mood_score', 'anxiety_score')
    search_fields = ('patient__username', 'notes')
    readonly_fields = ('timestamp',)
    
    def needs_attention(self, obj):
        return obj.needs_attention
    needs_attention.boolean = True


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """Admin for check-ins."""
    
    list_display = ('patient', 'scheduled_date', 'checkin_type', 'completed', 'completion_date')
    list_filter = ('checkin_type', 'completed', 'scheduled_date')
    search_fields = ('patient__username',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin for recommendations."""
    
    list_display = ('patient', 'category', 'is_ai_generated', 'created_by_psychologist', 'patient_completed', 'patient_helpful')
    list_filter = ('category', 'is_ai_generated', 'is_active', 'patient_completed')
    search_fields = ('patient__username', 'recommendation_text')


@admin.register(ConsentRecord)
class ConsentRecordAdmin(SimpleHistoryAdmin):
    """Admin for consent records."""
    
    list_display = ('patient', 'can_share_with_doctor', 'can_share_chat_with_doctor', 'can_share_with_psychologist', 'can_use_for_research')
    list_filter = ('can_share_with_doctor', 'can_share_with_psychologist', 'can_use_for_research')
    search_fields = ('patient__username',)
