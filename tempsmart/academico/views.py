from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion, CursoUsuario, ProgramaAcademico, Publicacion, Comentario, PerfilUsuario, Icono
from .serializers import (
    CursoSerializer, 
    HorarioSerializer, 
    TareaSerializer, 
    TipoHorarioSerializer, 
    NotificacionSerializer,
    CursoUsuarioSerializer,
    ProgramaAcademicoSerializer,
    PublicacionSerializer,
    ComentarioSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    IconoSerializer,
    PerfilUsuarioSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

# ViewSets para los iconos
class IconoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Icono.objects.all()
    serializer_class = IconoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ViewSets para los modelos
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CursoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = CursoUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra los cursos asignados solo al usuario autenticado
        usuario = self.request.user
        return CursoUsuario.objects.filter(usuario=usuario)

    def perform_create(self, serializer):
        # Obtén el `curso_id` del cuerpo de la solicitud
        curso_id = self.request.data.get('curso_id')

        # Valida que se proporcionó un `curso_id`
        if not curso_id:
            raise serializers.ValidationError({"error": "El campo 'curso_id' es requerido."})

        # Verifica que el curso exista
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            raise serializers.ValidationError({"error": "Curso no encontrado."})

        # Asegúrate de que el usuario no esté asignado ya a este curso
        if CursoUsuario.objects.filter(usuario=self.request.user, curso=curso).exists():
            raise serializers.ValidationError({"error": "Este curso ya está asignado al usuario."})

        # Crea el registro de CursoUsuario asignado al usuario autenticado
        serializer.save(usuario=self.request.user, curso=curso, creado_por_usuario=True)

class HorarioViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Horario.objects.filter(usuario=usuario)

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Tarea.objects.filter(curso__usuario=usuario)

    @action(detail=False, methods=['get'], url_path='curso/(?P<curso_id>[^/.]+)')
    def tareas_por_curso(self, request, curso_id=None):
        usuario = request.user
        try:
            curso_usuario = CursoUsuario.objects.get(usuario=usuario, curso__id=curso_id)
        except CursoUsuario.DoesNotExist:
            return Response({'detail': 'No estás inscrito en este curso.'}, status=404)

        tareas = Tarea.objects.filter(curso=curso_usuario)
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)

class TipoHorarioViewSet(viewsets.ModelViewSet):
    queryset = TipoHorario.objects.all()
    serializer_class = TipoHorarioSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class ProgramaAcademicoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaAcademico.objects.all()
    serializer_class = ProgramaAcademicoSerializer

class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar comentarios por publicación
        publicacion_id = self.request.query_params.get('publicacion')
        if publicacion_id:
            return Comentario.objects.filter(publicacion_id=publicacion_id)
        return Comentario.objects.all()

    def destroy(self, request, *args, **kwargs):
        # Permitir eliminar solo si el usuario es el dueño del comentario
        comentario = self.get_object()
        if comentario.usuario != request.user:
            return Response({'error': 'No tienes permiso para eliminar este comentario.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
# Registro de usuario
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  
            return Response({
                'user': serializer.data,
                'token': token.key  
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login de usuario
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        username = user_data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)

class UsuarioActualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        perfil = None

        if hasattr(user, 'perfil'):
            perfil = PerfilUsuarioSerializer(user.perfil).data

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "perfil": perfil
        })