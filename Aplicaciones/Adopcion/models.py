from django.db import models
from datetime import date
from Aplicaciones.Mascota.models import Mascota

class Adopcion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    nombre_adoptante = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)

    fecha = models.DateField(default=date.today)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def save(self, *args, **kwargs):
        # Si la adopcion fue aceptada, marcar la mascota como adoptada
        if self.estado == 'aceptada':
            self.mascota.adoptado = True
            self.mascota.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_adoptante} - {self.mascota.nombre} ({self.estado})"
