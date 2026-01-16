# Lia for a Woman 🌸

**Sistema de Apoyo Psico-Clínico para Mujeres Oncológicas**

Un sistema integral basado en Django que integra chatbot conversacional, módulo clínico, módulo psicosocial, y paneles diferenciados por rol para proporcionar apoyo integral a mujeres con cáncer.

---

## 📋 Descripción

Lia for a Woman es una plataforma de apoyo que NO reemplaza al profesional de salud, sino que asiste, organiza y acompaña a pacientes oncológicas proporcionando:

- 🤖 **Chatbot Lia**: Conversaciones empáticas con detección de riesgos
- 🏥 **Módulo Clínico**: Seguimiento de síntomas y alertas automáticas
- 💜 **Módulo Psicosocial**: Apoyo emocional y seguimiento psicológico
- 👥 **Conexión Paciente-Equipo**: Comunicación segura con médicos y psicólogos
- 🔐 **Privacidad**: Control de consentimiento estilo GDPR

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- PostgreSQL (opcional, por defecto usa SQLite)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone <repository-url>
cd "Lia Woman"
```

### Paso 2: Crear Entorno Virtual

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

1. Copiar el archivo de ejemplo:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

2. Editar `.env` con tus configuraciones:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Para PostgreSQL (opcional):
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=lia_db
# DB_USER=lia_user
# DB_PASSWORD=tu_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Paso 5: Aplicar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 6: Crear Superusuario

```bash
python manage.py createsuperuser
```

### Paso 7: Ejecutar el Servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: **http://127.0.0.1:8000/**

---

## 👥 Roles del Sistema

### 1. **Paciente** (Mujer Oncológica)
- Interactúa con Lia (chat/voz)
- Registra síntomas y estado emocional
- Recibe recomendaciones personalizadas
- Visualiza su proceso de forma simple

### 2. **Médico**
- Accede a datos clínicos relevantes
- Ve evolución de síntomas
- Recibe alertas generadas por IA
- Respeta consentimiento para datos sensibles

### 3. **Psicólogo/a**
- Accede a métricas psicoemocionales
- Visualiza patrones de estado emocional
- Crea recomendaciones personalizadas
- Apoya procesos de adherencia

---

## 📱 Funcionalidades Principales

### Chatbot "Lia"
- Conversación empática en español
- Detección de palabras clave de riesgo (CRITICAL/HIGH/MEDIUM/LOW)
- Generación automática de alertas
- Soporte para voz (Web Speech API - Chrome/Edge)

### Módulo Clínico
- Registro de síntomas con intensidad (1-10)
- Línea de tiempo clínica
- Sistema de alertas automáticas
- Notificaciones por email para médicos

### Módulo Psicosocial
- Check-ins emocionales con escalas Likert
- Análisis de tendencias (IMPROVING/STABLE/DECLINING)
- Recomendaciones IA + recomendaciones de psicólogos
- Gestión de consentimiento de datos

---

## 🛠️ Estructura del Proyecto

```
lia-for-a-woman/
│
├── lia_project/         # Configuración principal de Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # Rutas principales
│   ├── wsgi.py          # WSGI para producción
│   └── asgi.py          # ASGI para async
│
├── users/               # Autenticación y usuarios
├── chatbot/             # Chatbot Lia
├── clinical/            # Módulo clínico
├── psychosocial/        # Módulo psicosocial
├── patient/             # Dashboard de paciente
├── doctor/              # Dashboard de médico
├── psychologist/        # Dashboard de psicólogo/a
├── api/                 # API REST
│
├── templates/           # Templates HTML globales
├── static/              # CSS, JS, imágenes
├── media/               # Archivos subidos por usuarios
├── docs/                # Documentación
│
├── requirements.txt     # Dependencias de Python
├── manage.py            # Utilidad de Django
└── README.md            # Este archivo
```

---

## 🔐 Seguridad y Privacidad

### Características de Seguridad:
- ✅ Autenticación basada en roles (Django Groups)
- ✅ Control de acceso con decoradores personalizados
- ✅ Consentimiento explícito para compartir datos
- ✅ Historial de auditoría (django-simple-history)
- ✅ Encriptación de campos sensibles
- ✅ Protección CSRF automática de Django

### Control de Consentimiento:
Los médicos **NO pueden** acceder a:
- Conversaciones de chat sin consentimiento del paciente
- Datos emocionales sin permiso explícito

---

## 📊 API REST

La API está disponible en `/api/` con autenticación por token.

### Endpoints Principales:

```bash
# Obtener token de autenticación
POST /api/auth/token/
Body: {"username": "usuario", "password": "contraseña"}

# Chat
GET  /api/chat/          # Historial de chat
POST /api/chat/          # Enviar mensaje

# Síntomas
GET  /api/symptoms/      # Listar síntomas
POST /api/symptoms/      # Reportar síntoma

# Emociones
GET  /api/emotions/      # Listar registros emocionales
POST /api/emotions/      # Registrar emoción

# Recomendaciones
GET  /api/recommendations/  # Ver recomendaciones
```

Ejemplo de uso:
```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"paciente1","password":"password"}'

# 2. Usar token en requests
curl http://localhost:8000/api/chat/ \
  -H "Authorization: Token <tu-token>"
```

---

## 🧪 Testing

### Ejecutar Tests:
```bash
python manage.py test
```

### Tests de Integración Manual:

1. **Registro y Login**
   - Registrar paciente, médico, y psicólogo
   - Verificar redirección a dashboard correcto

2. **Chatbot**
   - Enviar "me duele mucho la cabeza" → Debe crear síntoma
   - Enviar "no aguanto más" → Debe crear alerta

3. **Módulo Clínico**
   - Reportar síntoma con intensidad 9 → Alerta visible en dashboard médico

4. **Módulo Psicosocial**
   - Completar check-in emocional
   - Verificar gráficos en dashboard de psicólogo

5. **Privacidad**
   - Desactivar consentimiento de chat
   - Verificar que médico no puede ver conversaciones

---

## 🎨 Tecnologías Utilizadas

### Backend:
- Django 4.2+ (Web Framework)
- Django REST Framework (API)
- PostgreSQL / SQLite (Base de datos)
- NLTK / TextBlob (NLP)

### Frontend:
- Django Templates
- Tailwind CSS
- JavaScript (Vanilla)
- Chart.js (Visualizaciones)
- Web Speech API (Voz)

### Seguridad:
- django-simple-history (Auditoría)
- django-encrypted-model-fields (Encriptación)
- django-cors-headers (CORS)

---

## 📝 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Acceder al shell de Django
python manage.py shell

# Recopilar archivos estáticos (para producción)
python manage.py collectstatic
```

---

## 🚧 Roadmap

### MVP (Actual):
- ✅ Chatbot con reglas basadas en keywords
- ✅ Detección de riesgos básica
- ✅ Dashboards diferenciados por rol
- ✅ Sistema de alertas
- ✅ Control de consentimiento

### Futuro:
- 🔜 Integración con LLM real (OpenAI/Anthropic)
- 🔜 Transcripción automática de voz
- 🔜 ML avanzado para análisis emocional
- 🔜 Notificaciones en tiempo real (WebSocket)
- 🔜 App móvil (React Native)

---

## 📄 Licencia

Este proyecto está desarrollado con fines educativos y de investigación.

---

## 👩‍💻 Contribuciones

Para contribuir:
1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📞 Soporte

Para preguntas o soporte:
- 📧 Email: support@liaforwoman.com
- 📖 Documentación: Ver carpeta `/docs`

---

## ⚠️ Importante

**Lia for a Woman es un sistema de apoyo y NO reemplaza el diagnóstico, tratamiento o consejo médico profesional. Siempre consulta con profesionales de la salud calificados para decisiones médicas.**

---

**Hecho con 💜 para apoyar a mujeres en su proceso oncológico**
