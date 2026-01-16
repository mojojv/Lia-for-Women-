"""
URL configuration for lia_project.

Main routing for Lia for a Woman system.
Routes organized by role and functionality.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # User authentication and management
    path('', include('users.urls')),
    
    # Chatbot interface
    path('chat/', include('chatbot.urls')),
    
    # Clinical module
    path('clinical/', include('clinical.urls')),
    
    # Psychosocial module
    path('psychosocial/', include('psychosocial.urls')),
    
    # Patient interface
    path('patient/', include('patient.urls')),
    
    # Doctor interface
    path('doctor/', include('doctor.urls')),
    
    # Psychologist interface
    path('psychologist/', include('psychologist.urls')),
    
    # REST API
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Lia for a Woman - Administración"
admin.site.site_title = "Lia Admin"
admin.site.index_title = "Panel de Administración"
