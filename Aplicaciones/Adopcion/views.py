from django.shortcuts import render, redirect, get_object_or_404
from .models import Adopcion
from Aplicaciones.Mascota.models import Mascota
from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


# AÑADE ESTA FUNCIÓN AL INICIO
@login_required
def inicioadopcion(request):
    listadoAdo = Adopcion.objects.all()
    return render(request, 'inicio3.html', {'adopciones': listadoAdo})


@login_required
def nuevaAdopcion(request):
    # Obtener mascotas no adoptadas
    mascotas = Mascota.objects.filter(adoptado=False)
    
    # Mascotas con imágenes para la galería (solo las no adoptadas con imagen)
    mascotas_con_imagen = []
    for mascota in mascotas:
        if mascota.imgMascota:  # Verificar que tenga imagen
            mascotas_con_imagen.append({
                'id': mascota.id,
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'get_especie_display': mascota.get_especie_display(),
                'edad': mascota.edad,
                'imgMascota': mascota.imgMascota
            })
    
    return render(request, 'nuevaAdopcion.html', {
        'mascotas': mascotas,
        'mascotas_con_imagen': mascotas_con_imagen
    })

@login_required
def guardarAdo(request):
    if request.method == 'POST':
        nombre_adoptante = request.POST.get('nombre_adoptante')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        mascota_id = request.POST.get('mascota')
        fecha_adopcion = date.today()

        # Validar que todos los campos estén presentes
        if not nombre_adoptante or not correo or not telefono or not mascota_id:
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('nuevaAdopcion')

        try:
            mascota = Mascota.objects.get(id=mascota_id)
            
            # Verificar que la mascota no esté ya adoptada
            if mascota.adoptado:
                messages.error(request, 'Esta mascota ya está adoptada')
                return redirect('nuevaAdopcion')
            
            # Crear la adopción
            Adopcion.objects.create(
                nombre_adoptante=nombre_adoptante,
                correo=correo,
                telefono=telefono,
                mascota=mascota,
                fecha=fecha_adopcion,
                estado='pendiente'
            )
            
            messages.success(request, 'Adopción agregada con éxito')
        except Mascota.DoesNotExist:
            messages.error(request, 'La mascota seleccionada no existe')
            return redirect('nuevaAdopcion')
        except ValidationError as e:
            messages.error(request, f"No se pudo agregar la adopción: {e}")
            return redirect('nuevaAdopcion')
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
            return redirect('nuevaAdopcion')

    return redirect('inicioadopcion')

@login_required
def eliminarAdopcion(request, id):
    eliminarAdo = get_object_or_404(Adopcion, id=id)
    
    # Si la adopción estaba aceptada, liberar la mascota
    if eliminarAdo.estado == 'aceptada':
        mascota = eliminarAdo.mascota
        mascota.adoptado = False
        mascota.save()
    
    eliminarAdo.delete()
    messages.success(request, 'Adopción eliminada con éxito')
    return redirect('inicioadopcion')

@login_required
def editarAdopcion(request, id):
    adopcionEditar = get_object_or_404(Adopcion, id=id)
    
    # Obtener mascotas no adoptadas + la mascota actual (para poder mantenerla si ya está adoptada)
    mascotas_disponibles = Mascota.objects.filter(adoptado=False)
    mascota_actual = adopcionEditar.mascota
    
    # Crear una lista que incluya mascotas no adoptadas + la mascota actual
    mascotas_list = list(mascotas_disponibles)
    if mascota_actual not in mascotas_list:
        mascotas_list.append(mascota_actual)
    
    # Para la galería de imágenes, mostrar todas las mascotas con imagen
    # excluyendo la mascota actual de la adopción que se está editando
    mascotas_con_imagen = Mascota.objects.filter(adoptado=False).exclude(imgMascota='').exclude(id=mascota_actual.id)
    
    return render(request, 'editarAdopcion.html', {
        'adopcionEditar': adopcionEditar, 
        'mascotas': mascotas_list,
        'mascotas_con_imagen': mascotas_con_imagen
    })

@login_required
def procesoEditarAdopcion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nombre_adoptante = request.POST.get('nombre_adoptante')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        mascota_id = request.POST.get('mascota')
        fecha_adopcion = date.today()

        # Validar campos
        if not all([id, nombre_adoptante, correo, telefono, mascota_id]):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('editarAdopcion', id=id)

        try:
            ado = get_object_or_404(Adopcion, id=id)
            nueva_mascota = Mascota.objects.get(id=mascota_id)
            
            # Si la adopción estaba aceptada y se cambia de mascota,
            # liberar la mascota anterior
            if ado.estado == 'aceptada' and ado.mascota != nueva_mascota:
                ado.mascota.adoptado = False
                ado.mascota.save()
            
            # Actualizar campos
            ado.nombre_adoptante = nombre_adoptante
            ado.correo = correo
            ado.telefono = telefono
            ado.mascota = nueva_mascota
            ado.fecha = fecha_adopcion
            
            ado.save()
            messages.success(request, 'Adopción editada con éxito')
            
        except Mascota.DoesNotExist:
            messages.error(request, 'La mascota seleccionada no existe')
            return redirect('editarAdopcion', id=id)
        except ValidationError as e:
            messages.error(request, f"No se pudo editar la adopción: {e}")
            return redirect('editarAdopcion', id=id)
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
            return redirect('editarAdopcion', id=id)

    return redirect('inicioadopcion')

@login_required
def aceptarAdopcion(request, id):
    ado = get_object_or_404(Adopcion, id=id)
    
    if ado.estado != 'pendiente':
        messages.warning(request, 'Esta adopción ya fue procesada')
        return redirect('inicioadopcion')
    
    # Verificar que la mascota no esté ya adoptada por otra adopción
    if ado.mascota.adoptado:
        messages.error(request, 'Esta mascota ya está adoptada')
        return redirect('inicioadopcion')

    ado.estado = 'aceptada'
    ado.mascota.adoptado = True
    ado.mascota.save()
    ado.save()
    
    messages.success(request, f'Adopción de {ado.mascota.nombre} aceptada')
    return redirect('inicioadopcion')

@login_required
def rechazarAdopcion(request, id):
    ado = get_object_or_404(Adopcion, id=id)
    
    if ado.estado != 'pendiente':
        messages.warning(request, 'Esta adopción ya fue procesada')
        return redirect('inicioadopcion')
    
    ado.estado = 'rechazada'
    ado.save()
    
    messages.success(request, f'Adopción de {ado.mascota.nombre} rechazada')
    return redirect('inicioadopcion')