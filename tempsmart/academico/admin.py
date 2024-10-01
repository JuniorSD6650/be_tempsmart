from django.contrib import admin
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion, Icono

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color', 'icono', 'docente')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'curso', 'dia_de_la_semana', 'hora_inicio', 'hora_fin', 'aula')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'fecha_vencimiento', 'curso')

@admin.register(TipoHorario)
class TipoHorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'leida', 'fecha_creacion')

@admin.register(Icono)
class IconoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen')
