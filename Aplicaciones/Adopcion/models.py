from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from Aplicaciones.Mascota.models import Mascota

class Adopcion(models.Model):
    nombre_adoptante = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        limit_choices_to={'adoptado': False}
    )

    fecha = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if self.mascota.adoptado:
            raise ValidationError("Esta mascota ya fue adoptada")

        super().save(*args, **kwargs)

        self.mascota.adoptado = True
        self.mascota.save()

    def __str__(self):
        return f"{self.nombre_adoptante} - {self.mascota.nombre}"
