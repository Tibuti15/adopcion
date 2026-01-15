from django.urls import path

from .views import login_view, registro_view, vista_mascotas, logout_view


urlpatterns = [
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('mascotas/', vista_mascotas, name='vista_mascotas'),
    path('logout/', logout_view, name='logout'),
]
