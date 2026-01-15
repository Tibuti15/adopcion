from django.shortcuts import render, redirect, get_object_or_404
from .models import Adopcion
from Aplicaciones.Mascota.models import Mascota
from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def inicioadopcion(request):
    listadoAdo = Adopcion.objects.all()
    return render(request, 'inicio3.html', {'adopciones': listadoAdo})

@login_required
def nuevaAdopcion(request):
    mascotas = Mascota.objects.filter(adoptado=False)
    return render(request, 'nuevaAdopcion.html', {'mascotas': mascotas})

@login_required
def guardarAdo(request):
    nombre_adoptante = request.POST['nombre_adoptante']
    correo = request.POST['correo']
    telefono = request.POST['telefono']
    mascota_id = request.POST['mascota']
    fecha_adopcion = date.today()

    mascota = Mascota.objects.get(id=mascota_id)

    try:
        Adopcion.objects.create(
            nombre_adoptante=nombre_adoptante,
            correo=correo,
            telefono=telefono,
            mascota=mascota,
            fecha=fecha_adopcion,
            estado='pendiente'
        )
        messages.success(request, 'Adopcion agregada con exito')
    except ValidationError as e:
        messages.error(request, f"No se pudo agregar la adopcion: {e}")
        return redirect('nuevaAdopcion')

    return redirect('inicioadopcion')

@login_required
def eliminarAdopcion(request, id):
    eliminarAdo = get_object_or_404(Adopcion, id=id)
    if eliminarAdo.estado == 'aceptada':
        mascota = eliminarAdo.mascota
        mascota.adoptado = False
        mascota.save()
    eliminarAdo.delete()
    messages.success(request, 'Adopcion eliminada con exito')
    return redirect('inicioadopcion')

@login_required
def editarAdopcion(request, id):
    adopcionEditar = get_object_or_404(Adopcion, id=id)
    mascotas = Mascota.objects.filter(adoptado=False) | Mascota.objects.filter(id=adopcionEditar.mascota.id)
    return render(request, 'editarAdopcion.html', {'adopcionEditar': adopcionEditar, 'mascotas': mascotas})

@login_required
def procesoEditarAdopcion(request):
    id = request.POST['id']
    nombre_adoptante = request.POST['nombre_adoptante']
    correo = request.POST['correo']
    telefono = request.POST['telefono']
    mascota_id = request.POST['mascota']
    fecha_adopcion = date.today()

    ado = get_object_or_404(Adopcion, id=id)
    nueva_mascota = Mascota.objects.get(id=mascota_id)

    if ado.estado == 'aceptada' and ado.mascota != nueva_mascota:
        ado.mascota.adoptado = False
        ado.mascota.save()

    ado.nombre_adoptante = nombre_adoptante
    ado.correo = correo
    ado.telefono = telefono
    ado.mascota = nueva_mascota
    ado.fecha = fecha_adopcion

    try:
        ado.save()
        messages.success(request, 'Adopcion editada con exito')
    except ValidationError as e:
        messages.error(request, f"No se pudo editar la adopcion: {e}")

    return redirect('inicioadopcion')

@login_required
def aceptarAdopcion(request, id):
    ado = get_object_or_404(Adopcion, id=id)
    if ado.estado != 'pendiente':
        messages.warning(request, 'Esta adopcion ya fue procesada')
        return redirect('inicioadopcion')

    ado.estado = 'aceptada'
    ado.mascota.adoptado = True
    ado.mascota.save()
    ado.save()
    messages.success(request, f'Adopcion de {ado.mascota.nombre} aceptada')
    return redirect('inicioadopcion')

@login_required
def rechazarAdopcion(request, id):
    ado = get_object_or_404(Adopcion, id=id)
    if ado.estado != 'pendiente':
        messages.warning(request, 'Esta adopcion ya fue procesada')
        return redirect('inicioadopcion')

    
    ado.estado = 'rechazada'
    ado.save()
    messages.success(request, f'Adopcion de {ado.mascota.nombre} rechazada')
    return redirect('inicioadopcion')
