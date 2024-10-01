# academico/serializers.py

from rest_framework import serializers
from .models import Curso, Horario, Tarea, TipoHorario, Notificacion

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

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Serializer para registro de usuario
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña solo es de escritura
        }

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            token = Token(user=user)
            token.save()
            return user
        except Exception as e:
            print(e)  # Imprimir el error para depuración
            raise serializers.ValidationError('Error al crear el usuario o el token.')


# Serializer para login de usuario
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise AuthenticationFailed('Credenciales incorrectas.')
        
        token, created = Token.objects.get_or_create(user=user)
        return {
            'username': user.username,
            'email': user.email,
            'token': token.key  # Asegúrate de devolver el token aquí
        }