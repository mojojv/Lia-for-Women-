"""
NLP service for chatbot.
Handles message processing, sentiment analysis, and risk detection.
"""
import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger('chatbot')


import re
import logging
import random
from typing import Dict, List, Tuple
from django.db.models import Q

logger = logging.getLogger('chatbot')

class ChatService:
    """
    Advanced NLP service for 'Lia'.
    Features: Context awareness, regex pattern matching, varied empathetic responses.
    """
    
    # --- RIESGO Y SEGURIDAD ---
    RISK_KEYWORDS = {
        'CRITICAL': [
            r'quiero morir', r'suicidar', r'acabar con todo', r'no vale la pena vivir',
            r'mejor muerta', r'matarme', r'pastillas para dormir', r'cortarme'
        ],
        'HIGH': [
            r'no aguanto m[áa]s', r'no puedo m[áa]s', r'dolor insoportable',
            r'no encuentro salida', r'desesperad[oa]', r'ayuda por favor'
        ],
        'MEDIUM': [
            r'muy triste', r'dolor intenso', r'dolor fuerte', r'muy mal',
            r'fatal', r'terrible', r'llorando', r'deprimid[oa]'
        ],
        'LOW': [
            r'triste', r'duele', r'cansada', r'agotada', r'molesta', r'aburrida'
        ]
    }
    
    # --- BASES DE CONOCIMIENTO Y RESPUESTAS ---
    RESPONSES = {
        'GREETING': [
            "¡Hola {name}! 🌸 Qué alegría verte de nuevo. ¿Cómo te sientes en este momento?",
            "Hola {name}, aquí estoy para ti. ¿Cómo ha ido tu día hasta ahora?",
            "Bienvenida de nuevo, {name}. Soy Lia. ¿En qué puedo acompañarte hoy?",
            "Hola {name}. Espero que estés teniendo un día tranquilo. Cuéntame, ¿cómo estás?",
        ],
        'PAIN_HIGH': [
            "Siento mucho que estés pasando por ese dolor tan fuerte. Es importante que no lo ignores. ¿Has tomado tu medicación habitual?",
            "Entiendo que el dolor es intenso. Por favor, trata de respirar profundo. ¿Podrías describir exactamente dónde se localiza?",
            "Lamento escuchar eso. Nadie debería sentir dolor así. ¿Del 1 al 10, dirías que es un 8 o más?",
        ],
        'PAIN_LOW': [
            "Entiendo, el dolor o molestia siempre es incómodo. ¿Crees que el descanso te ayudaría?",
            "Lamento que tengas esa molestia. ¿Has notado si empeora con algún movimiento?",
            "Tomo nota de tu malestar. A veces el cuerpo nos pide pausa. ¿Puedes descansar un poco ahora?",
        ],
        'EMOTION_SAD': [
            "Te abrazo a la distancia. Es completamente válido sentirse triste. ¿Quieres contarme qué provocó este sentimiento?",
            "Está bien no estar bien a veces. Aquí estoy para escucharte sin juzgar. Desahógate si lo necesitas.",
            "La tristeza es una emoción pesada, pero no tienes que cargarla sola. Estoy aquí contigo.",
            "Tómate tu tiempo. Llorar o sentirse bajo de energía es parte de ser humano. ¿Puedo hacer algo para apoyarte?",
        ],
        'EMOTION_ANXIETY': [
            "Respira conmigo... Inhala despacio... Exhala. La ansiedad puede ser abrumadora, pero pasará. ¿Qué te preocupa en este instante?",
            "Siento que estás inquieta. Tratemos de enfocarnos en el presente. ¿Puedes nombrar 3 cosas que ves a tu alrededor?",
            "La ansiedad a veces nos miente sobre el futuro. Vamos paso a paso. Estoy aquí contigo, segura.",
        ],
        'JOY': [
            "¡Qué maravilla leer eso! 🎉 Me encanta saber que te sientes bien.",
            "¡Eso suena fantástico! Es importante celebrar estos momentos de bienestar.",
            "¡Me alegra muchísimo! Gracias por compartir algo positivo conmigo, ilumina mi día virtual.",
        ],
        'GRATITUDE': [
            "No tienes nada que agradecer, es mi propósito acompañarte. 💜",
            "¡Para eso estoy! Me hace feliz poder ser útil.",
            "Gracias a ti por confiar en mí y abrirte.",
        ],
        'UNKNOWN': [
            "Te escucho atentamente. Cuéntame un poco más para entender mejor.",
            "Entiendo. ¿Y cómo te hace sentir eso?",
            "Vaya... continua, por favor. Estoy aquí para leerte.",
            "Mm, entiendo. ¿Hay algo específico en lo que te gustaría que profundicemos?",
            "A veces es difícil ponerlo en palabras, pero lo estás haciendo muy bien. Cuéntame más.",
        ]
    }

    def process_message(self, message: str, user=None) -> Dict:
        """
        Procesa el mensaje con lógica mejorada de Lia 2.0.
        """
        message_lower = message.lower().strip()
        user_name = user.first_name if user and user.first_name else (user.username if user else "amiga")
        
        # 1. Detección de Riesgo
        risk_level, detected_keywords = self._detect_risk(message_lower)
        
        # 2. Análisis de Sentimiento y Tema
        intent = self._detect_intent(message_lower)
        
        # 3. Generación de Respuesta
        response = self._generate_response(intent, risk_level, user_name, message_lower)
        
        # 4. Acción Sugerida (si aplica)
        suggested_action = self._suggest_action(risk_level, message_lower)
        
        # Determinar flag de sentimiento para la DB
        sentiment_flag = self._map_risk_to_sentiment(risk_level, intent)

        return {
            'response': response,
            'sentiment': sentiment_flag,
            'risk_level': risk_level,
            'risk_keywords': detected_keywords,
            'suggested_action': suggested_action
        }
    
    def _detect_risk(self, message: str) -> Tuple[str, List[str]]:
        """Detecta riesgo usando Expresiones Regulares."""
        detected = []
        
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            for pattern in self.RISK_KEYWORDS[level]:
                if re.search(pattern, message):
                    detected.append(pattern.replace(r'', '')) # Clean regex chars for display
                    # Si es crítico o alto, retornamos inmediatamente
                    if level in ['CRITICAL', 'HIGH']:
                        return level, detected
        
        if detected:
            # Retornar el nivel más alto encontrado (ya manejado por el orden del loop pero por seguridad)
            return 'MEDIUM' if any(k in self.RISK_KEYWORDS['MEDIUM'] for k in detected) else 'LOW', detected
            
        return 'NONE', []

    def _detect_intent(self, message: str) -> str:
        """Clasifica la intención del mensaje."""
        if any(g in message for g in ['hola', 'buenos d', 'buenas t', 'buenas n', 'hi', 'hey']):
            return 'GREETING'
        if any(w in message for w in ['gracias', 'agradez', 'amable']):
            return 'GRATITUDE'
        if any(w in message for w in ['bien', 'feliz', 'contenta', 'genial', 'mejor', 'alegr']):
            return 'JOY'
        if any(w in message for w in ['triste', 'llora', 'pena', 'depre', 'sola', 'vacía']):
            return 'EMOTION_SAD'
        if any(w in message for w in ['ansiedad', 'miedo', 'nervios', 'angustia', 'panico', 'tiembla']):
            return 'EMOTION_ANXIETY'
        if any(w in message for w in ['dolor', 'duele', 'ardor', 'punzada', 'migraña']):
            return 'PAIN' # Se refinará con el nivel de severidad luego
            
        return 'UNKNOWN'

    def _generate_response(self, intent: str, risk_level: str, name: str, message: str) -> str:
        """Selecciona una respuesta empática y variada."""
        
        # Prioridad 1: Crisis
        if risk_level == 'CRITICAL':
            return (f"{name}, escucho mucho dolor en tus palabras y me preocupas. Tu vida es valiosa. "
                    "Por favor, déjame contactar a ayuda profesional ahora mismo. No estás sola.")
        elif risk_level == 'HIGH':
            return ("Siento que estás al límite. Es importante no cargar esto sola. "
                    "Voy a notificar a tu médico para que revisen tu caso prioritariamente. Respira conmigo un momento.")

        # Prioridad 2: Dolor Físico (si no es crisis)
        if intent == 'PAIN' or 'dolor' in message:
            # Determinar intensidad por contexto simple
            if any(x in message for x in ['mucho', 'insoportable', 'horrible', 'fuerte', '8', '9', '10']):
                return random.choice(self.RESPONSES['PAIN_HIGH'])
            return random.choice(self.RESPONSES['PAIN_LOW'])

        # Prioridad 3: Emociones Específicas
        if intent == 'EMOTION_SAD':
            return random.choice(self.RESPONSES['EMOTION_SAD'])
        if intent == 'EMOTION_ANXIETY':
            return random.choice(self.RESPONSES['EMOTION_ANXIETY'])
        
        # Prioridad 4: Intenciones Generales
        if intent == 'GREETING':
            return random.choice(self.RESPONSES['GREETING']).format(name=name)
        if intent == 'GRATITUDE':
            return random.choice(self.RESPONSES['GRATITUDE'])
        if intent == 'JOY':
            return random.choice(self.RESPONSES['JOY'])
            
        # Fallback inteligente con "Ecos"
        # Si no entendemos, intentamos reflejar algo que dijo
        if len(message) > 10 and '?' not in message:
             return random.choice(self.RESPONSES['UNKNOWN'])
        
        return "Te escucho. ¿Podrías contarme un poco más?"

    def _suggest_action(self, risk_level: str, message: str) -> str:
        if risk_level == 'CRITICAL':
            return "URGENTE: Activar protocolo de crisis/suicidio."
        if risk_level == 'HIGH':
            return "PRIORIDAD: Valoración médica/psicológica en <24h."
        if 'dolor' in message and risk_level == 'MEDIUM':
            return "Seguimiento: Ajuste de analgesia o revisión física."
        return None

    def _map_risk_to_sentiment(self, risk_level: str, intent: str) -> str:
        if risk_level in ['CRITICAL', 'HIGH']: return 'ALERT'
        if risk_level == 'MEDIUM': return 'CONCERN'
        if intent == 'JOY': return 'POSITIVE'
        if intent in ['EMOTION_SAD', 'EMOTION_ANXIETY']: return 'CONCERN'
        return 'NEUTRAL'

chat_service = ChatService()
