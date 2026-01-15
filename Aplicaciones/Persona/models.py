from django.db import models

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    edad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    foto = models.FileField(upload_to='persona', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

