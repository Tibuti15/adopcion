from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Aplicaciones.Mascota.models import Mascota

# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('vista_mascotas')  # ← redirige al listado de mascotas
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

# Vista de registro
def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        username = request.POST['username']
        password = request.POST['password']
        confirmar = request.POST['confirmar']

        if password != confirmar:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=nombre,
                last_name=apellido
            )
            messages.success(request, 'Usuario creado correctamente. Inicia sesión.')
            return redirect('login')
    return render(request, 'registrar.html')

# Vista principal para todos los usuarios (listado de mascotas)
@login_required
def vista_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'listaMascotas.html', {
        'usuario': request.user,
        'mascotas': mascotas
    })

# Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')
