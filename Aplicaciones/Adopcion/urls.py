from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioadopcion, name='inicioadopcion'),
    path('nuevaAdopcion/', views.nuevaAdopcion, name='nuevaAdopcion'),
    path('guardarAdo/', views.guardarAdo, name='guardarAdo'),
    path('editarAdopcion/<int:id>/', views.editarAdopcion, name='editarAdopcion'),
    path('procesoEditarAdopcion/', views.procesoEditarAdopcion, name='procesoEditarAdopcion'),
    path('eliminarAdopcion/<int:id>/', views.eliminarAdopcion, name='eliminarAdopcion'),
    path('aceptarAdopcion/<int:id>/', views.aceptarAdopcion, name='aceptarAdopcion'),
    path('rechazarAdopcion/<int:id>/', views.rechazarAdopcion, name='rechazarAdopcion'),
]
