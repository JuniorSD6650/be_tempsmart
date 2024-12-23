from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Registrar los ViewSets existentes y nuevos
router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet)
router.register(r'cursos-usuario', views.CursoUsuarioViewSet, basename='cursousuario')
router.register(r'horarios', views.HorarioViewSet, basename='horarios')
router.register(r'tareas', views.TareaViewSet, basename='tarea')
router.register(r'tipos-horario', views.TipoHorarioViewSet)
router.register(r'notificaciones', views.NotificacionViewSet)
router.register(r'programas-academicos', views.ProgramaAcademicoViewSet) 
router.register(r'publicaciones', views.PublicacionViewSet) 
router.register(r'comentarios', views.ComentarioViewSet, basename='comentario')  
router.register(r'iconos', views.IconoViewSet)

# Nuevas rutas para registro e inicio de sesión
urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.UserRegisterView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('usuarios/me/', views.UsuarioActualView.as_view(), name='usuario_actual'),
]
