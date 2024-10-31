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
    IconoSerializer
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
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra las tareas por el usuario autenticado
        usuario = self.request.user
        return Tarea.objects.filter(curso__usuario=usuario)


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
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

# Registro de usuario
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Crear o recuperar el token del usuario
            return Response({
                'user': serializer.data,
                'token': token.key  # Incluye el token en la respuesta
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
