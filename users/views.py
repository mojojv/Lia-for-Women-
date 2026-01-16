"""
Views for user authentication and profile management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction

from .forms import CustomUserCreationForm, CustomLoginForm, ProfileForm
from .models import CustomUser, Profile


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard_redirect')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Create profile automatically
                Profile.objects.create(user=user)
                
                messages.success(
                    request,
                    f'¡Bienvenida/o {user.first_name}! Tu cuenta ha sido creada exitosamente.'
                )
                login(request, user)
                return redirect('users:dashboard_redirect')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard_redirect')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenida/o de nuevo, {user.first_name}!')
                return redirect('users:dashboard_redirect')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:login')


@login_required
def dashboard_redirect(request):
    """Redirect user to appropriate dashboard based on role."""
    user = request.user
    
    if user.is_patient():
        return redirect('patient:dashboard')
    elif user.is_doctor():
        return redirect('doctor:dashboard')
    elif user.is_psychologist():
        return redirect('psychologist:dashboard')
    else:
        messages.error(request, 'Rol de usuario no válido.')
        return redirect('users:login')


@login_required
def profile_view(request):
    """View and edit user profile."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)


@login_required
def home_view(request):
    """Landing page after login - shows welcome message."""
    return render(request, 'users/home.html')
