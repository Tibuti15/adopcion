from django.shortcuts import render,redirect
import os
from Aplicaciones.Persona.models import Persona
from django.contrib import messages
from django.conf import settings


def inicioPersonas(request):
    listadoPersona=Persona.objects.all()
    return render (request,"inicio2.html",{'personas': listadoPersona})

def nuevaPersona(request):
    return render(request,"nuevaPersona.html")

def guardarPersona (request):
    nombres=request.POST ["nombres"]
    apellidos=request.POST["apellidos"]
    edad=request.POST["edad"]
    telefono=request.POST["telefono"]
    correo=request.POST["correo"]
    foto=request.FILES.get("foto")


    nuevaPersona = Persona.objects.create(nombres=nombres,apellidos=apellidos,
        edad=edad,telefono=telefono,correo=correo,foto=foto)
    #Mensaje de confirmacion
    messages.success(request,"Persona guardado exitosamente")
    return redirect('/inicio2/')
 
def eliminarPersona (request,id):
    personaEliminar = Persona.objects.get(id=id)

    
    if personaEliminar.foto:
        ruta_foto = os.path.join(settings.MEDIA_ROOT, personaEliminar.foto.name)
        if os.path.exists(ruta_foto):
            os.remove(ruta_foto)

    personaEliminar.delete()
    messages.success(request,"Persona eliminado exitosamente")
    return redirect('/inicio2/')


def editarPersona (request,id):
    personaEditar = Persona.objects.get(id=id)
    return render (request,'editarPersona.html',{'personaEditar':personaEditar})

def procesarEdicionPersona(request):
    id=request.POST['id']
    nombres=request.POST ["nombres"]
    apellidos=request.POST["apellidos"]
    edad=request.POST["edad"]
    telefono=request.POST["telefono"]
    correo=request.POST["correo"]
    foto=request.FILES.get("foto")
      
    #creacion del objeto
    persona=Persona.objects.get(id=id)#buscando la persona que se quiere editar por id
    persona.nombres=nombres
    persona.apellidos=apellidos
    persona.edad=edad
    persona.telefono=telefono
    persona.correo=correo
    # Eliminar y reemplazar logo
    if foto:  # Solo si se subió una nueva
        if persona.foto:
            ruta_foto = os.path.join(settings.MEDIA_ROOT, persona.foto.name)
            if os.path.exists(ruta_foto):
                os.remove(ruta_foto)
        persona.foto = foto

    #mensaje de confirmacion
    messages.success(request,"Persona actualizado exitosamente")
    return redirect('/inicio2/')