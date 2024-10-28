from rest_framework import serializers
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion, CursoUsuario, ProgramaAcademico, Publicacion, Comentario, PerfilUsuario
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
    class Meta:
        model = CursoUsuario
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

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
    class Meta:
        model = Comentario
        fields = '__all__'

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'

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
