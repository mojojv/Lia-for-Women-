# Arquitectura del Sistema - Lia for a Woman

## Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Django Templates)               │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Patient    │  │   Doctor     │  │  Psychologist     │  │
│  │  Dashboard  │  │   Dashboard  │  │   Dashboard       │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                    DJANGO MIDDLEWARE LAYER                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Auth/Session │  │     CSRF     │  │  Audit History   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                       DJANGO APPS                            │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Users  │  │ Chatbot │  │ Clinical │  │ Psychosocial │  │
│  └─────────┘  └─────────┘  └──────────┘  └──────────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Patient │  │ Doctor  │  │Psycholog.│  │     API      │  │
│  └─────────┘  └─────────┘  └──────────┘  └──────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                     SERVICES LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Chat Service │  │Alert Service │  │ Emotion Service  │  │
│  │  (NLP/Rules) │  │  (Notif.)    │  │ (Trends/AI Rec.) │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                    DATABASE (PostgreSQL/SQLite)              │
│  ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Users   │  │ Symptoms  │  │ Emotions │  │  Alerts  │  │
│  │   Chat    │  │ Timeline  │  │ CheckIns │  │ Consent  │  │
│  └───────────┘  └───────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

##  Componentes Principales

### 1. **Capa de Presentación (Frontend)**

**Tecnología**: Django Templates + Tailwind CSS + JavaScript

**Dashboards Diferenciados**:
- `patient/dashboard.html`: Wellness indicator, quick actions, chat access
- `doctor/dashboard.html`: Patient list with alerts, clinical monitoring  
- `psychologist/dashboard.html`: Emotional metrics, trend charts

**Características**:
- Responsive design (mobile-first con Tailwind)
- Empathetic UX (soft colors, friendly messages)
- Web Speech API integration (voice input/output)
- Chart.js for data visualization

---

### 2. **Capa de Aplicación (Django Apps)**

#### 2.1 Users App
**Responsabilidad**: Autenticación y gestión de usuarios

**Modelos**:
- `CustomUser`: Extends AbstractUser + role field (PATIENT/DOCTOR/PSYCHOLOGIST)
- `Profile`: Extended profile with assigned_doctor, assigned_psychologist

**Servicios**:
- Role-based decorators (`@patient_only`, `@doctor_only`, etc.)
- Consent checking (`@patient_consent_required`)

#### 2.2 Chatbot App
**Responsabilidad**: Interacción conversacional con Lia

**Modelos**:
- `ChatInteraction`: message_text, bot_response, sentiment_flag, risk_keywords
- `VoiceMemo`: audio_file, transcription (future)

**Servicios**:
- `ChatService`: Keyword detection, empathetic response generation
- Risk levels: NONE/LOW/MEDIUM/HIGH/CRITICAL

#### 2.3 Clinical App
**Responsabilidad**: Seguimiento médico y alertas

**Modelos**:
- `SymptomReport`: symptom_type, intensity (1-10), reported_via
- `Alert`: alert_type, severity, message, suggested_action
- `ClinicalTimeline`: event_type, event_description, event_date

**Servicios**:
- `SymptomService`: Symptom processing from chat/forms
- `AlertService`: Alert creation, email notifications
- `TimelineService`: Clinical event logging

#### 2.4 Psychosocial App
**Responsabilidad**: Apoyo emocional y psicológico

**Modelos**:
- `EmotionLog`: mood_score, anxiety_score, energy_score (Likert 1-10)
- `CheckIn`: scheduled_date, completed, adherence tracking
- `Recommendation`: AI-generated or psychologist-created
- `ConsentRecord`: Privacy controls

**Servicios**:
- `EmotionService`: Trend analysis (IMPROVING/STABLE/DECLINING)
- `RecommendationService`: Rule-based recommendation generation
- `ConsentService`: Data access permission checking

#### 2.5 Patient App
**Responsabilidad**: Dashboard para pacientes

**Features**:
- Wellness indicator (GREEN/YELLOW/RED)
- Quick access to chat, symptom reporting, check-ins
- Recent activities overview

#### 2.6 Doctor App
**Responsabilidad**: Dashboard para médicos

**Features**:
- Patient list with alert counts (CRITICAL/HIGH/MEDIUM)
- Detailed patient view (symptoms, timeline, alerts)
- Consent-based access to chat conversations

#### 2.7 Psychologist App
**Responsabilidad**: Dashboard para psicólogos

**Features**:
- Emotional metrics visualization
- Trend charts (Chart.js)
- Recommendation creation
- Adherence tracking

#### 2.8 API App
**Responsabilidad**: REST API for future mobile app

**Endpoints**:
- `/api/chat/`: Chat interactions
- `/api/symptoms/`: Symptom reports
- `/api/emotions/`: Emotion logs
- `/api/recommendations/`: Recommendations

**Authentication**: Token-based (DRF)

---

### 3. **Capa de Servicios (Business Logic)**

**Principio**: Lógica de negocio separada de vistas

**Servicios Principales**:

1. **chat_service.ChatService**
   - `process_message()`: NLP keyword detection + response generation
   - `_detect_risk()`: Risk level classification
   - `_generate_response()`: Context-aware empathetic responses

2. **clinical.services.AlertService**
   - `create_symptom_alert()`: Auto-alert from severe symptoms
   - `create_chat_alert()`: Auto-alert from risky chat
   - `_send_alert_email()`: Email notification to doctor

3. **psychosocial.services.EmotionService**
   - `analyze_trend()`: 7/30-day emotion trend analysis
   - `get_average_scores()`: Average mood/anxiety/energy
   - `check_emotional_alert()`: Alert if mood critically low

4. **psychosocial.services.RecommendationService**
   - `generate_recommendation_for_patient()`: Rule-based AI recs
   - `check_adherence()`: Check-in completion rate

5. **psychosocial.services.ConsentService**
   - `can_access_data()`: Permission checking before data access

---

### 4. **Capa de Datos (Models)**

**ORM**: Django ORM

**Database**: PostgreSQL (production) / SQLite (development)

**Características**:
- Audit trail: django-simple-history on all sensitive models
- Encryption: django-encrypted-model-fields for sensitive data
- Indexing: Strategic indexes on foreign keys and timestamp fields
- JSON fields: For flexible data like risk_keywords, emotion_scores

**Key Relationships**:
```
CustomUser (1) ←→ (1) Profile
CustomUser (1) ←→ (N) ChatInteraction
CustomUser (1) ←→ (N) SymptomReport
CustomUser (1) ←→ (N) EmotionLog
CustomUser (1) ←→ (N) Alert
SymptomReport (1) ←→ (N) Alert (related_symptom)
ChatInteraction (1) ←→ (N) Alert (related_chat)
```

---

## Flujos de Datos Principales

### Flujo 1: Interacción de Chat

```
1. Patient sends message via chat interface
   ↓
2. AJAX POST to /chat/send/
   ↓
3. chatbot.views.send_message()
   ↓
4. chat_service.process_message()
   ├─ Detect risk keywords
   ├─ Determine sentiment
   └─ Generate empathetic response
   ↓
5. Save ChatInteraction to DB
   ↓
6. IF risk_level >= HIGH:
   ├─ Create Alert (clinical.services.alert_service)
   ├─ Send email to doctor
   └─ Log in audit trail
   ↓
7. IF pain mentioned:
   └─ Create SymptomReport (clinical.services.symptom_service)
   ↓
8. Return JSON response to frontend
```

### Flujo 2: Reporte de Síntoma

```
1. Patient fills symptom form
   ↓
2. POST to /clinical/report/
   ↓
3. clinical.views.report_symptom()
   ↓
4. Save SymptomReport (intensity, type, description)
   ↓
5. symptom_service.check_symptom_alerts()
   ↓
6. IF intensity >= 8:
   ├─ Create Alert (SYMPTOM_SEVERE)
   ├─ Set severity based on intensity
   ├─ Send email to assigned doctor
   └─ Update ClinicalTimeline
   ↓
7. Redirect to patient dashboard
```

### Flujo 3: Check-in Emocional

```
1. Patient submits emotion check-in form
   ↓
2. POST to /psychosocial/checkin/
   ↓
3. psychosocial.views.emotion_checkin()
   ↓
4. Save EmotionLog (mood, anxiety, energy scores)
   ↓
5. Mark CheckIn as completed
   ↓
6. emotion_service.check_emotional_alert()
   ↓
7. IF mood <= 3 OR anxiety >= 8:
   ├─ Create Alert (EMOTION_CRISIS)
   └─ Notify psychologist
   ↓
8. Suggest AI recommendation if trend declining
```

### Flujo 4: Acceso a Datos (Doctor/Psychologist)

```
1. Doctor clicks on patient
   ↓
2. doctor.views.patient_detail(patient_id)
   ↓
3. consent_service.can_access_data(patient, doctor, 'chat')
   ↓
4. IF consent = True:
   └─ Show chat messages
   ELSE:
   └─ Show "Requiere consentimiento" message
   ↓
5. Load symptoms, alerts, timeline (always accessible with clinical consent)
```

---

## Seguridad y Privacidad

### Autenticación y Autorización

**Mecanismo**: Django Authentication + Custom Decorators

**Niveles de Control**:
1. **Authentication**: `@login_required`
2. **Role-based**: `@patient_only`, `@doctor_only`, `@psychologist_only`
3. **Consent-based**: `@patient_consent_required('can_share_with_doctor')`

### Encriptación

- **Passwords**: bcrypt (Django default)
- **Sensitive fields**: django-encrypted-model-fields
- **HTTPS**: TLS 1.3 en producción

### Auditoría

**django-simple-history** tracks:
- Who changed what
- When
- Previous values
- Immutable log

---

## Escalabilidad

### Optimizaciones Actuales

- **Database indexing** on frequent queries (patient_id, timestamp)
- **Select_related / Prefetch_related** in views to minimize queries
- **Pagination** in API (20 items per page)
- **Static file serving** via CDN (production)

### Preparado para:

- **Caching**: Redis integration points ready
- **Async tasks**: Celery for email sending, ML processing
- **Load balancing**: Stateless design, session in DB
- **Microservices**: Clear service boundaries, can extract to separate services

---

## Tecnologías y Dependencias

### Backend Core
- **Django 4.2+**: Web framework
- **PostgreSQL**: Production database
- **Gunicorn**: WSGI server (production)

### APIs y Extensiones
- **Django REST Framework**: REST API
- **django-cors-headers**: API CORS
- **django-simple-history**: Audit trail
- **django-encrypted-model-fields**: Field encryption

### NLP y ML
- **NLTK**: Natural Language Toolkit (keyword matching)
- **TextBlob**: Sentiment analysis (future enhancement)
- **pandas/numpy**: Data processing for ML (future)

### Frontend
- **Tailwind CSS**: Utility-first CSS
- **Chart.js**: Data visualization
- **Web Speech API**: Voice recognition/synthesis

---

## Deployment

### Development
```bash
python manage.py runserver
# SQLite database
# DEBUG=True
```

### Production (Recommended)
```bash
# PostgreSQL database
# DEBUG=False
# ALLOWED_HOSTS configured
# Static files served via nginx/CDN
# gunicorn with workers
# HTTPS with SSL certificate
```

---

## Monitoreo y Logging

### Logs Configurados

```python
LOGGING = {
    'chatbot': INFO level → File + Console
    'clinical': INFO level → File + Console  
    'django': INFO level → File + Console
}
```

**Log Locations**: `logs/lia.log`

### Métricas Recomendadas (Futuro)

- Alert response time
- Chat message volume
- User engagement rates
- System uptime
- API latency

---

**Última actualización**: Enero 2024
**Versión de Arquitectura**: MVP 1.0
