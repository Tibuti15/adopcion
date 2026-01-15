from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os

from .models import Mascota

def inicio(request):
    mascotas = Mascota.objects.all()
    return render(request, 'listaMascotas.html', {'mascotas': mascotas})

@login_required
def nuevaMascota(request):
    especies = Mascota.ESPECIE_CHOICES
    return render(request, 'nuevaMascota.html', {'especies': especies})

@login_required
def guardarMascota(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')
        edad = request.POST.get('edad')
        imgMascota = request.FILES.get('imgMascota')

        if not codigo or not nombre or not especie or not edad:
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('nuevaMascota')

        if Mascota.objects.filter(codigo=codigo).exists():
            messages.error(request, 'Ya existe una mascota con este codigo')
            return redirect('nuevaMascota')

        Mascota.objects.create(
            codigo=codigo,
            nombre=nombre,
            especie=especie,
            edad=edad,
            imgMascota=imgMascota
        )

        messages.success(request, 'Mascota agregada correctamente')
        return redirect('inicio')

    messages.error(request, 'Metodo no permitido')
    return redirect('inicio')

@login_required
def editarMascota(request, id):
    mascotaEditar = get_object_or_404(Mascota, id=id)
    especies = Mascota.ESPECIE_CHOICES
    return render(request, 'editarMascota.html', {'mascotaEditar': mascotaEditar, 'especies': especies})

@login_required
def procesarEdicionMascota(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        mascota = get_object_or_404(Mascota, id=id)

        mascota.codigo = request.POST.get('codigo')
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.edad = request.POST.get('edad')

        imgMascotaAct = request.FILES.get('imgMascota')
        if imgMascotaAct:
            mascota.imgMascota = imgMascotaAct

        
        if Mascota.objects.exclude(id=mascota.id).filter(codigo=mascota.codigo).exists():
            messages.error(request, 'Ya existe otra mascota con este codigo')
            return redirect('editarMascota', id=mascota.id)

        mascota.save()
        messages.success(request, 'Mascota editada correctamente')
        return redirect('inicio')

    messages.error(request, 'Error al editar la mascota')
    return redirect('inicio')

@login_required
def eliminarMascota(request, id):
    mascotaEliminar = get_object_or_404(Mascota, id=id)

    if mascotaEliminar.imgMascota:
        ruta_img = os.path.join(settings.MEDIA_ROOT, mascotaEliminar.imgMascota.name)
        if os.path.isfile(ruta_img):
            os.remove(ruta_img)

    mascotaEliminar.delete()
    messages.success(request, 'Mascota eliminada correctamente')
    return redirect('inicio')


