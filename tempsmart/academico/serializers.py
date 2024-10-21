# academico/serializers.py

from rest_framework import serializers
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion
from django.core.validators import RegexValidator  # Agrega esta importación
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Serializers de los modelos de tu aplicación
class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
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

# Serializer para registro de usuario
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$',
                message="La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, un número y un carácter especial."
            )
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Verificar si el correo ya está registrado
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('El correo ya está registrado.')
        
        # Verificar si el nombre de usuario ya está registrado
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('El nombre de usuario ya está en uso.')

        try:
            user = User(
                username=validated_data['username'],
                email=validated_data['email']
            )
            # Asegúrate de usar set_password para encriptar la contraseña
            user.set_password(validated_data['password'])
            user.save()

            token, created = Token.objects.get_or_create(user=user)
            return user
        except Exception as e:
            print(e)  # Imprimir el error para depuración
            raise serializers.ValidationError('Error al crear el usuario o el token.')

# Serializer para login de usuario
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Autenticar usuario
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Credenciales incorrectas.')

        # Verificar si el usuario está activo
        if not user.is_active:
            raise AuthenticationFailed('Esta cuenta está deshabilitada.')

        # Generar o recuperar el token
        token, created = Token.objects.get_or_create(user=user)

        return {
            'username': user.username,
            'email': user.email,
            'token': token.key
        }
