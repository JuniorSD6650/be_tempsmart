from django.contrib import admin
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion, Icono, CursoUsuario, ProgramaAcademico, Publicacion, Comentario, PerfilUsuario

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color', 'icono', 'docente')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'curso', 'dia_de_la_semana', 'hora_inicio', 'hora_fin', 'aula')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'fecha_vencimiento', 'curso', 'icono')  # Añadido 'icono' para las tareas

@admin.register(TipoHorario)
class TipoHorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'leida', 'fecha_creacion')

@admin.register(Icono)
class IconoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen')

@admin.register(CursoUsuario)
class CursoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'creado_por_usuario')

@admin.register(ProgramaAcademico)
class ProgramaAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('curso', 'titulo', 'fecha_creacion')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('publicacion', 'usuario', 'contenido', 'fecha_creacion')

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'programa_academico', 'codigo_estudiante')
