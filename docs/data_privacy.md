# Privacidad y Protección de Datos - Lia for a Woman

## Principios de Privacidad

### 1. **Privacy by Design**

La privacidad está integrada en la arquitectura del sistema desde el diseño:

- Datos sensibles encriptados en base de datos
- Acceso basado en roles con permisos granulares
- Consentimiento explícito antes de compartir datos
- Auditoría completa de accesos a datos

### 2. **Minimización de Datos**

Solo recopilamos lo estrictamente necesario:

**Datos Recopilados**:
- Información de usuario (nombre, email, rol)
- Datos clínicos (síntomas reportados)
- Datos emocionales (check-ins, estado de ánimo)
- Conversaciones con chatbot
- Archivos de voz (opcional)

**NO Recopilamos**:
- Información financiera
- Datos de navegación web fuera del sistema
- Información de terceros sin consentimiento
- Datos de localización en tiempo real

### 3. **Control del Usuario**

Las pacientes tienen control total sobre sus datos:

- ✅ Ver todos sus datos
- ✅ Modificar configuración de privacidad
- ✅ Revocar consentimientos en cualquier momento
- ✅ Solicitar eliminación de datos (derecho al olvido)
- ✅ Exportar sus datos en formato legible

---

## Sistema de Consentimiento

### Tipos de Consentimiento

1. **Compartir Datos Clínicos con Médico** (Default: ✅)
   - Síntomas reportados
   - Alertas generadas
   - Línea de tiempo clínica

2. **Compartir Conversaciones de Chat con Médico** (Default: ❌)
   - Mensajes con Lia
   - Análisis de sentimiento
   - Keywords detectados

3. **Compartir Datos Emocionales con Psicólogo/a** (Default: ✅)
   - Check-ins emocionales
   - Escalas de ánimo/ansiedad/energía
   - Tendencias psicológicas

4. **Uso de Datos para Investigación** (Default: ❌)
   - Datos anonimizados
   - Solo para estudios aprobados éticamente
   - Paciente puede revocar en cualquier momento

### Cambio de Consentimiento

- Paciente puede cambiar preferencias en cualquier momento
- Cambios se aplican inmediatamente
- Historial de cambios se registra (auditoría)
- Profesionales ven claramente si NO tienen acceso

---

## Seguridad de Datos

### Encriptación

- **En tránsito**: HTTPS/TLS 1.3 (producción)
- **En reposo**: Campos sensibles encriptados en BD
- **Contraseñas**: Hash con algoritmo bcrypt (Django default)

### Control de Acceso

**Matriz de Permisos**:

| Datos                | Paciente | Médico (con consentimiento) | Psicólogo/a (con consientimiento) | Admin |
|---------------------|----------|---------------------------|----------------------------------|-------|
| Datos clínicos      | ✅ Total | ✅ Lectura                | ❌ No                             | ✅ Total |
| Conversaciones chat | ✅ Total | ⚠️ Con consentimiento     | ❌ No                             | ✅ Total |
| Datos emocionales   | ✅ Total | ❌ No                      | ⚠️ Con consentimiento            | ✅ Total |
| Alertas             | ✅ Lectura | ✅ Lectura/Escritura    | ✅ Lectura                        | ✅ Total |

### Auditoría

**Registro de Accesos**:
- Quién accedió
- Qué datos accedió
- Cuándo
- Desde dónde (IP)
- Qué cambios realizó

Estos registros son inmutables (no se pueden borrar ni modificar).

---

## Cumplimiento Normativo

### Inspiración GDPR (Unión Europea)

Aunque Lia puede no estar sujeta directamente a GDPR, implementamos sus principios:

1. **Derecho a la Información**: Política de privacidad clara
2. **Derecho de Acceso**: Paciente puede ver todos sus datos
3. **Derecho de Rectificación**: Paciente puede corregir datos
4. **Derecho al Olvido**: Paciente puede solicitar eliminación
5. **Derecho a la Portabilidad**: Exportación de datos en JSON
6. **Derecho a Oposición**: Paciente puede oponerse a procesamiento

### HIPAA-like (Datos de Salud - USA)

Principios implementados:
- Mínimo necesario: Solo acceso necesario para función
- Salvaguardas técnicas: Encriptación, auditoría
- Salvaguardas administrativas: Políticas de acceso
- Notificación de brechas: Protocolo definido

---

## Retención de Datos

### Políticas de Retención

| Tipo de Dato              | Retención                     | Después de Eliminación              |
|---------------------------|------------------------------|-------------------------------------|
| Datos de usuario activo   | Ilimitado (mientras usa app) | -                                   |
| Datos de cuenta inactiva  | 2 años sin login             | Notificación, luego anonimización   |
| Conversaciones de chat    | 5 años                       | Eliminación completa               |
| Alertas críticas          | 7 años (legal)               | Anonimización, conservar stats      |
| Logs de auditoría         | 10 años                      | Conservar permanentemente          |

### Eliminación de Cuenta

Cuando un paciente solicita eliminar su cuenta:

1. **Inmediato**: 
   - Bloqueo de acceso
   - Datos personales anonimizados

2. **30 días**: 
   - Período de gracia (puede recuperar)

3. **Después de 30 días**:
   - Eliminación permanente de datos personales
   - Conservación de datos anonimizados para estadísticas

---

## Manejo de Brechas de Seguridad

### Protocolo de Respuesta

1. **Detección** (0-24h)
   - Identificar alcance de la brecha
   - Contener el problema

2. **Notificación** (24-72h)
   - Notificar a usuarios afectados
   - Notificar a autoridades si aplica
   - Transparencia sobre datos comprometidos

3. **Mitigación** (72h-1 semana)
   - Cambiar credenciales comprometidas
   - Parchear vulnerabilidad
   - Reforzar seguridad

4. **Prevención** (Continua)
   - Análisis de causa raíz
   - Implementar medidas preventivas
   - Entrenamiento de equipo

---

## Compartir Datos con Terceros

### Política Estricta

Lia **NO comparte** datos con terceros excepto:

1. **Proveedores de Infraestructura** (necesario para funcionar)
   - Hosting (ej: AWS, Google Cloud)
   - Email (ej: SendGrid para alertas)
   - **Todos** firmaron acuerdos de confidencialidad

2. **Autoridades Legales**
   - Solo bajo orden judicial válida
   - Notificamos al usuario (si legalmente permitido)

3. **Investigación Académica**
   - **Solo** datos anonimizados
   - **Solo** con consentimiento explícito del paciente
   - **Solo** proyectos aprobados por comité de ética

### Nunca Compartimos Para:
- ❌ Publicidad
- ❌ Venta de datos
- ❌ Marketing directo
- ❌ Perfilado comercial

---

## Derechos del Usuario

### Cómo Ejercer tus Derechos

1. **Ver tus datos**: 
   - Panel de usuario → "Mis Datos"

2. **Exportar datos**:
   - Panel de usuario → "Exportar Datos" → Descargar JSON

3. **Modificar consentimientos**:
   - Panel de usuario → "Privacidad" → Ajustar preferencias

4. **Eliminar cuenta**:
   - Panel de usuario → "Configuración" → "Eliminar Cuenta"
   - O contactar: privacy@liaforwoman.com

5. **Reportar problema de privacidad**:
   - 📧 privacy@liaforwoman.com
   - Respuesta en 48 horas

---

## Transparencia

### Cambios en esta Política

- Notificaremos cambios importantes por email
- Histórico de versiones disponible
- 30 días para revisar antes de aplicación

### Auditorías Externas

- Auditoría de seguridad anual (recomendado)
- Publicación de resumen de hallazgos
- Plan de acción para mejoras

---

## Contacto

**Data Protection Officer (DPO)**:
- 📧 dpo@liaforwoman.com
- 📞 [Teléfono de contacto]

Para preguntas sobre privacidad:
- 📧 privacy@liaforwoman.com

---

**Última actualización**: Enero 2024
**Vigencia**: Esta política está vigente desde el lanzamiento del MVP
