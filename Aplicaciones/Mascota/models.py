from django.db import models

class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Otro', 'Otro'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    edad = models.PositiveIntegerField()
    adoptado = models.BooleanField(default=False)

    imgMascota = models.ImageField(upload_to='imgMascota/', blank=True, null=True)

    def __str__(self):
        return self.nombre

