import os
import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Icono(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.nombre

# Usar la señal post_delete para eliminar el archivo de imagen después de eliminar la instancia
@receiver(post_delete, sender=Icono)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Elimina el archivo de imagen cuando se elimina la instancia del modelo."""
    if instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, help_text="Código de color en formato hexadecimal")
    icono = models.ForeignKey(Icono, on_delete=models.SET_NULL, blank=True, null=True)
    docente = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', self.color):
            raise ValidationError("El código de color debe estar en formato hexadecimal, por ejemplo, #FFFFFF.")

    def __str__(self):
        return self.nombre

class TipoHorario(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Horario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoHorario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    dia_de_la_semana = models.IntegerField(choices=[(i, f"Día {i}") for i in range(1, 8)])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=100, blank=True, null=True, help_text="Formato: P1-401 (Pabellón 1, Piso 4, Aula 401)")

    def clean(self):
        # Validación de superposición de horarios
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")
        
        # Validación del día de la semana
        if self.dia_de_la_semana < 1 or self.dia_de_la_semana > 7:
            raise ValidationError("El día de la semana debe estar entre 1 (lunes) y 7 (domingo).")

    def __str__(self):
        return f"{self.curso.nombre} - {self.dia_de_la_semana} de {self.hora_inicio} a {self.hora_fin}"

class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_vencimiento = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notificación para {self.usuario.username} - {'Leída' if self.leida else 'No leída'}"
