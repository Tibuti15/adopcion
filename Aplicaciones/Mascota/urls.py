from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nuevaMascota/', views.nuevaMascota, name='nuevaMascota'),
    path('guardarMascota/', views.guardarMascota, name='guardarMascota'),
    path('editarMascota/<int:id>/', views.editarMascota, name='editarMascota'),
    path('procesarEdicionMascota/', views.procesarEdicionMascota, name='procesarEdicionMascota'),
    path('eliminarMascota/<int:id>/', views.eliminarMascota, name='eliminarMascota'),
    path('reporteAdopcion/', views.reporteAdopcion, name='reporte_adopcion'),
]
