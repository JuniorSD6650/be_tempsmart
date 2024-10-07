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
from rest_framework.parsers import MultiPartParser, FormParser
import pdfplumber
from django.db import transaction
from django.contrib.auth.models import User
from .utils import extract_courses_info  # Importamos la función de utilidades

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

# Nueva vista para procesar el PDF
class UploadPDFView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado."}, status=401)

        pdf_file = request.FILES.get('file')

        if not pdf_file:
            return Response({"error": "No se ha proporcionado ningún archivo PDF."}, status=400)

        try:
            with pdfplumber.open(pdf_file) as pdf:
                text_completo = ""
                horarios = []
                for page in pdf.pages:
                    text = page.extract_text()
                    text_completo += text + "\n"  # Acumular el texto de cada página

                # Procesar el texto del PDF para extraer los cursos y horarios
                cursos_info = extract_courses_info(text_completo)

                # Verificar si se extrajeron datos
                if not cursos_info:
                    return Response({"error": "No se pudo extraer información del PDF.", "texto": text_completo}, status=400)

                # Guardar los cursos y horarios en la base de datos
                self.save_courses_and_schedules(cursos_info, request.user)

            return Response({
                "message": "Datos de horarios procesados y guardados con éxito.",
                "texto": text_completo
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @transaction.atomic
    def save_courses_and_schedules(self, cursos_info, user):
        """
        Guarda los cursos y horarios extraídos en la base de datos, evitando duplicados y actualizando los existentes.
        """
        tipo_horario, _ = TipoHorario.objects.get_or_create(nombre="Académico")  # Usamos "Académico" como tipo fijo

        for curso_data in cursos_info:
            curso, created = Curso.objects.update_or_create(
                nombre=curso_data['nombre'],
                defaults={
                    'descripcion': curso_data.get('descripcion', ''),
                    'color': curso_data.get('color', '#FFFFFF'),
                    'docente': curso_data.get('docente', '')
                }
            )

            for horario in curso_data['horarios']:
                dia_semana = horario.get('dia_de_la_semana')

                if dia_semana is None:
                    continue

                # Guardamos o actualizamos el horario
                Horario.objects.update_or_create(
                    usuario=user,
                    curso=curso,
                    dia_de_la_semana=dia_semana,
                    hora_inicio=horario['hora_inicio'],
                    defaults={
                        'hora_fin': horario['hora_fin'],
                        'aula': horario.get('aula', ''),
                        'tipo': tipo_horario
                    }
                )
