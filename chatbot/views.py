"""
Views for chatbot interface.
"""
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import ChatInteraction, VoiceMemo
from .services import chat_service
from users.decorators import patient_only

logger = logging.getLogger('chatbot')


@login_required
@patient_only
def chat_interface(request):
    """Main chat interface view."""
    # Get recent chat history
    recent_chats = ChatInteraction.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:50]
    
    context = {
        'recent_chats': recent_chats,
        'user_name': request.user.first_name or request.user.username
    }
    
    return render(request, 'chatbot/chat_interface.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request):
    """
    Process chat message and return bot response.
    AJAX endpoint.
    """
    message = request.POST.get('message', '').strip()
    
    if not message:
        return JsonResponse({
            'success': False,
            'error': 'Mensaje vacío'
        }, status=400)
    
    try:
        # Process message with chat service
        result = chat_service.process_message(
            message,
            user_name=request.user.first_name
        )
        
        # Save interaction to database
        interaction = ChatInteraction.objects.create(
            user=request.user,
            message_text=message,
            bot_response=result['response'],
            sentiment_flag=result['sentiment'],
            risk_keywords_detected=result['risk_keywords']
        )
        
        # If high risk, create alert
        if result['risk_level'] in ['CRITICAL', 'HIGH']:
            from clinical.services import alert_service
            alert_service.create_chat_alert(
                patient=request.user,
                interaction=interaction,
                risk_level=result['risk_level'],
                suggested_action=result['suggested_action']
            )
        
        # Also log symptom if pain mentioned
        if 'dolor' in message.lower():
            from clinical.services import symptom_service
            symptom_service.create_symptom_from_chat(
                patient=request.user,
                message=message,
                interaction=interaction
            )
        
        logger.info(f"Chat interaction saved - User: {request.user.username}, Risk: {result['risk_level']}")
        
        return JsonResponse({
            'success': True,
            'response': result['response'],
            'sentiment': result['sentiment'],
            'timestamp': interaction.timestamp.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error procesando el mensaje. Por favor intenta de nuevo.'
        }, status=500)


@login_required
def chat_history(request):
    """View full chat history."""
    chats = ChatInteraction.objects.filter(
        user=request.user
    ).order_by('-timestamp')
    
    context = {
        'chats': chats
    }
    
    return render(request, 'chatbot/chat_history.html', context)


@login_required
@require_http_methods(["POST"])
def upload_voice_memo(request):
    """
    Handle voice memo uploads.
    Future: Implement transcription service.
    """
    if 'audio_file' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': 'No se encontró archivo de audio'
        }, status=400)
    
    audio_file = request.FILES['audio_file']
    
    try:
        voice_memo = VoiceMemo.objects.create(
            user=request.user,
            audio_file=audio_file
        )
        
        logger.info(f"Voice memo uploaded - User: {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'memo_id': voice_memo.id,
            'message': 'Audio guardado exitosamente'
        })
        
    except Exception as e:
        logger.error(f"Error uploading voice memo: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error guardando el audio'
        }, status=500)
