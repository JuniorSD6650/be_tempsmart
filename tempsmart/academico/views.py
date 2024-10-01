from rest_framework import viewsets
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion
from .serializers import (
    CursoSerializer, 
    HorarioSerializer, 
    TareaSerializer, 
    TipoHorarioSerializer, 
    NotificacionSerializer,
    UserRegisterSerializer,
    UserLoginSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

# ViewSets para los modelos
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

class TipoHorarioViewSet(viewsets.ModelViewSet):
    queryset = TipoHorario.objects.all()
    serializer_class = TipoHorarioSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
