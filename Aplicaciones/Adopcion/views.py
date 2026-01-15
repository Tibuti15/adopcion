from django.shortcuts import render, redirect
from .models import Adopcion
from Aplicaciones.Mascota.models import Mascota
from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError

def inicioadopcion(request):
    listadoAdo = Adopcion.objects.all()
    return render(request, 'inicio3.html', {'adopciones': listadoAdo})


def nuevaAdopcion(request):
    mascotas = Mascota.objects.filter(adoptado=False)
    return render(request, 'nuevaAdopcion.html', {'mascotas': mascotas})


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
            fecha=fecha_adopcion
        )
        messages.success(request, 'Adopcion agregada con exito')
    except ValidationError as e:
        messages.error(request, f"No se pudo agregar la adopcion: {e}")
        return redirect('/nuevaAdopcion')

    return redirect('/inicio3')


def eliminarAdopcion(request, id):
    eliminarAdo = Adopcion.objects.get(id=id)
    mascota = eliminarAdo.mascota
    mascota.adoptado = False
    mascota.save()
    eliminarAdo.delete()
    messages.success(request, 'Adopción eliminada con exito')
    return redirect('/inicio3')


def editarAdopcion(request, id):
    adopcionEditar = Adopcion.objects.get(id=id)
    mascotas = Mascota.objects.filter(adoptado=False) | Mascota.objects.filter(id=adopcionEditar.mascota.id)
    return render(request, 'editarAdopcion.html', {'adopcionEditar': adopcionEditar, 'mascotas': mascotas})


def procesoEditarAdopcion(request):
    id = request.POST['id']
    nombre_adoptante = request.POST['nombre_adoptante']
    correo = request.POST['correo']
    telefono = request.POST['telefono']
    mascota_id = request.POST['mascota']
    fecha_adopcion = date.today()

    ado = Adopcion.objects.get(id=id)
    nueva_mascota = Mascota.objects.get(id=mascota_id)

    if ado.mascota != nueva_mascota:
        ado.mascota.adoptado = False
        ado.mascota.save()

    ado.nombre_adoptante = nombre_adoptante
    ado.correo = correo
    ado.telefono = telefono
    ado.mascota = nueva_mascota
    ado.fecha = fecha_adopcion

    try:
        ado.save()
        messages.success(request, 'Adopcion editada con éxito')
    except ValidationError as e:
        messages.error(request, f"No se pudo editar la adopcion: {e}")

    return redirect('/inicio3')
