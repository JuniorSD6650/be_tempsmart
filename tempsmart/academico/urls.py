from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Registrar los ViewSets existentes y nuevos
router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet)
router.register(r'cursos-usuario', views.CursoUsuarioViewSet)  # Nueva vista para los cursos del usuario
router.register(r'horarios', views.HorarioViewSet)
router.register(r'tareas', views.TareaViewSet)
router.register(r'tipos-horario', views.TipoHorarioViewSet)
router.register(r'notificaciones', views.NotificacionViewSet)
router.register(r'programas-academicos', views.ProgramaAcademicoViewSet)  # Nueva vista para programas académicos
router.register(r'publicaciones', views.PublicacionViewSet)  # Nueva vista para las publicaciones
router.register(r'comentarios', views.ComentarioViewSet)  # Nueva vista para los comentarios

# Nuevas rutas para registro e inicio de sesión
urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.UserRegisterView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
]
