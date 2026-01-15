from django.urls import path 
from . import views
urlpatterns = [
    path('',views.inicioPersonas),
    path('nuevaPersona',views.nuevaPersona),
    path('guardarPersona',views.guardarPersona),
    path('eliminarPersona/<id>',views.eliminarPersona),
    path('editarPersona/<id>',views.editarPersona),
    path('procesarEdicionPersona/',views.procesarEdicionPersona),
    
]