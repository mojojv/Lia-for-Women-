"""
Admin configuration for chatbot app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ChatInteraction, VoiceMemo


@admin.register(ChatInteraction)
class ChatInteractionAdmin(SimpleHistoryAdmin):
    """Admin interface for chat interactions."""
    
    list_display = ('user', 'timestamp', 'sentiment_flag', 'is_risky', 'message_preview')
    list_filter = ('sentiment_flag', 'timestamp')
    search_fields = ('user__username', 'message_text', 'bot_response')
    readonly_fields = ('timestamp',)
    
    def message_preview(self, obj):
        """Show first 50 characters of message."""
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Preview'
    
    def is_risky(self, obj):
        """Show risk indicator."""
        return obj.is_risky
    is_risky.boolean = True
    is_risky.short_description = 'Riesgo detectado'


@admin.register(VoiceMemo)
class VoiceMemoAdmin(admin.ModelAdmin):
    """Admin interface for voice memos."""
    
    list_display = ('user', 'created_at', 'duration_seconds', 'has_transcription')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'transcription')
    readonly_fields = ('created_at',)
    
    def has_transcription(self, obj):
        """Show if transcription exists."""
        return bool(obj.transcription)
    has_transcription.boolean = True
    has_transcription.short_description = 'Transcrito'
