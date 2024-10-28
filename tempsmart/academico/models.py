from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import os
import re

# Programa Academico
class ProgramaAcademico(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Perfil de usuario con campos adicionales
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    programa_academico = models.ForeignKey(ProgramaAcademico, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_estudiante = models.CharField(max_length=20, null=True, blank=True)  # Código de estudiante opcional

    def __str__(self):
        return self.usuario.username

# Icono para los cursos y tareas
class Icono(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100, help_text="Nombre del icono de MUI-ICONS (ej. ClassIcon, EditIcon)")

    def __str__(self):
        return self.nombre

@receiver(post_delete, sender=Icono)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Elimina el archivo de imagen cuando se elimina la instancia del modelo."""
    if instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)

# Curso general asociado a un programa académico
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, help_text="Código de color en formato hexadecimal")
    icono = models.ForeignKey(Icono, on_delete=models.SET_NULL, blank=True, null=True)
    docente = models.CharField(max_length=100, blank=True, null=True)  # Campo opcional para el docente
    programa_academico = models.ForeignKey(ProgramaAcademico, on_delete=models.CASCADE, related_name="cursos_generales", null=True, blank=True)

    def clean(self):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', self.color):
            raise ValidationError("El código de color debe estar en formato hexadecimal, por ejemplo, #FFFFFF.")

    def __str__(self):
        return self.nombre

# Cursos personalizados de cada usuario (pueden ser seleccionados de cursos generales o creados por ellos)
class CursoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cursos_personales")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="cursos_asignados")
    creado_por_usuario = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.nombre}"

# Tipos de horarios
class TipoHorario(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

# Horarios donde los usuarios asignan sus cursos personales
class Horario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoHorario, on_delete=models.CASCADE)
    curso = models.ForeignKey(CursoUsuario, on_delete=models.CASCADE)  # Relacionado con los cursos personales del usuario
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
        return f"{self.curso.curso.nombre} - {self.dia_de_la_semana} de {self.hora_inicio} a {self.hora_fin}"

# Tareas asignadas a los cursos, ahora con íconos
class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_vencimiento = models.DateField()
    curso = models.ForeignKey(CursoUsuario, on_delete=models.CASCADE)  # Relacionado con los cursos personales del usuario
    icono = models.ForeignKey(Icono, on_delete=models.SET_NULL, null=True, blank=True)  # Icono para la tarea
    
    def __str__(self):
        return self.titulo

# Foro: Publicaciones de temas para el examen, solo creadas por el administrador (superusuario)
class Publicacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="publicaciones")
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"

# Comentarios en las publicaciones del foro, creados por los estudiantes
class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario por {self.usuario.username} en {self.publicacion.titulo}"

# Notificaciones
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notificación para {self.usuario.username} - {'Leída' if self.leida else 'No leída'}"
