from rest_framework import serializers
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion, CursoUsuario, ProgramaAcademico, Publicacion, Comentario, PerfilUsuario, Icono
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Serializers de los modelos
class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class CursoUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.id')
    curso = CursoSerializer(read_only=True)

    class Meta:
        model = CursoUsuario
        fields = ['id', 'usuario', 'curso', 'creado_por_usuario']

class HorarioSerializer(serializers.ModelSerializer):
    # Campos que son de solo lectura (para visualización)
    curso = serializers.CharField(source='curso.curso.nombre', read_only=True)
    color = serializers.CharField(source='curso.curso.color', read_only=True)
    docente = serializers.CharField(source='curso.curso.docente', allow_null=True, read_only=True)
    dia = serializers.SerializerMethodField(read_only=True)  
    horaInicio = serializers.TimeField(source='hora_inicio', format="%H:%M", read_only=True)  
    horaFin = serializers.TimeField(source='hora_fin', format="%H:%M", read_only=True)  

    # Campos de escritura
    curso_id = serializers.PrimaryKeyRelatedField(queryset=CursoUsuario.objects.all(), source='curso', write_only=True)
    dia_de_la_semana = serializers.IntegerField(write_only=True) 
    hora_inicio = serializers.TimeField(write_only=True)  
    hora_fin = serializers.TimeField(write_only=True) 

    class Meta:
        model = Horario
        fields = [
            'id', 'curso', 'color', 'docente', 'dia', 'horaInicio', 'horaFin', 'aula',
            'curso_id', 'dia_de_la_semana', 'hora_inicio', 'hora_fin', 'usuario', 'tipo'
        ]

    def get_dia(self, obj):
        # Convertir dia_de_la_semana a nombre del día
        dias_semana = {
            1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves',
            5: 'Viernes', 6: 'Sábado', 7: 'Domingo'
        }
        return dias_semana.get(obj.dia_de_la_semana, 'Desconocido')

class TareaSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source='curso.curso.nombre', read_only=True)
    icono_nombre = serializers.CharField(source='icono.nombre', read_only=True)
    icono_imagen = serializers.CharField(source='icono.imagen', read_only=True)

    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'fecha_vencimiento', 'curso', 'curso_nombre', 'icono', 'icono_nombre', 'icono_imagen']

class TipoHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHorario
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

class ProgramaAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaAcademico
        fields = '__all__'

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)  # Nombre del usuario
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)  # ID del usuario

    class Meta:
        model = Comentario
        fields = ['id', 'publicacion', 'contenido', 'fecha_creacion', 'usuario_nombre', 'usuario_id']

    def create(self, validated_data):
        # Asocia el usuario autenticado al comentario
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'

class IconoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icono
        fields = ['id', 'nombre', 'imagen']

# Serializer para registro de usuario, con campos extra para perfil
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$',
            message="La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, un número y un carácter especial."
        )]
    )
    programa_academico = serializers.PrimaryKeyRelatedField(queryset=ProgramaAcademico.objects.all(), required=False)
    codigo_estudiante = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'programa_academico', 'codigo_estudiante']

    def create(self, validated_data):
        perfil_data = {
            'programa_academico': validated_data.pop('programa_academico', None),
            'codigo_estudiante': validated_data.pop('codigo_estudiante', None)
        }

        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        PerfilUsuario.objects.create(
            usuario=user,
            programa_academico=perfil_data['programa_academico'],
            codigo_estudiante=perfil_data['codigo_estudiante']
        )

        token, created = Token.objects.get_or_create(user=user)
        return user

# Serializer para login de usuario
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Credenciales incorrectas.')

        if not user.is_active:
            raise AuthenticationFailed('Esta cuenta está deshabilitada.')

        token, created = Token.objects.get_or_create(user=user)

        return {
            'username': user.username,
            'email': user.email,
            'token': token.key
        }
