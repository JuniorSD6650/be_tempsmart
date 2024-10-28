from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from academico.models import ProgramaAcademico, PerfilUsuario, Curso, Icono, TipoHorario
from django.core.files import File
import os

class Command(BaseCommand):
    help = "Crea usuarios, cursos, iconos, superusuario de prueba y tipo de horario académico"

    def handle(self, *args, **kwargs):
        # Crear el programa académico
        programa, created = ProgramaAcademico.objects.get_or_create(nombre="Ingeniería de Sistemas e Informática")
        if created:
            self.stdout.write(self.style.SUCCESS(f"Programa académico {programa.nombre} creado."))

        # Crear el superusuario
        superuser_data = {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin1234'}
        if not User.objects.filter(username=superuser_data['username']).exists():
            User.objects.create_superuser(superuser_data['username'], superuser_data['email'], superuser_data['password'])
            self.stdout.write(self.style.SUCCESS(f"Superusuario {superuser_data['username']} creado"))
        else:
            self.stdout.write(self.style.WARNING(f"Superusuario {superuser_data['username']} ya existía"))

        # Crear el tipo de horario "Académico"
        tipo_horario, created = TipoHorario.objects.get_or_create(nombre="Académico")
        if created:
            self.stdout.write(self.style.SUCCESS(f"Tipo de horario '{tipo_horario.nombre}' creado"))
        else:
            self.stdout.write(self.style.WARNING(f"Tipo de horario '{tipo_horario.nombre}' ya existía"))

        # Crear 5 usuarios de prueba
        usuarios_data = [
            {'username': 'gflores', 'email': 'gflores@example.com'},
            {'username': 'paulanichols', 'email': 'paulanichols@example.com'},
            {'username': 'samantha53', 'email': 'samantha53@example.com'},
            {'username': 'alyssa49', 'email': 'alyssa49@example.com'},
            {'username': 'davidhopkins', 'email': 'davidhopkins@example.com'}
        ]

        for user_data in usuarios_data:
            user, created = User.objects.get_or_create(username=user_data['username'], defaults={'email': user_data['email'], 'password': 'password123'})
            if created:
                PerfilUsuario.objects.create(usuario=user, programa_academico=programa)
                self.stdout.write(self.style.SUCCESS(f"Usuario {user.username} creado"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuario {user.username} ya existía"))

        # Lista de cursos predefinidos
        cursos_data = [
            {'nombre': 'Lenguaje I', 'descripcion': 'Curso general sobre habilidades de lenguaje.'},
            {'nombre': 'Matemática Básica I', 'descripcion': 'Curso introductorio de matemáticas básicas.'},
            {'nombre': 'Métodos y Técnicas de Estudio', 'descripcion': 'Curso sobre métodos y técnicas para mejorar el estudio.'},
            {'nombre': 'Psicología General', 'descripcion': 'Curso introductorio a la psicología.'},
            {'nombre': 'Introducción a la Ingeniería de Sistemas e Informática', 'descripcion': 'Curso introductorio a la ingeniería de sistemas.'},
            {'nombre': 'Ética y Liderazgo', 'descripcion': 'Curso sobre principios éticos y liderazgo.'},
            {'nombre': 'Lenguaje II', 'descripcion': 'Curso avanzado sobre habilidades de lenguaje.'},
            {'nombre': 'Matemática Básica II', 'descripcion': 'Curso avanzado de matemáticas básicas.'},
            {'nombre': 'Ecología y Protección del Medio Ambiente', 'descripcion': 'Curso sobre ecología y protección ambiental.'},
            {'nombre': 'Sociología General', 'descripcion': 'Curso introductorio a la sociología.'},
            {'nombre': 'Tecnología Informática', 'descripcion': 'Curso sobre el uso de tecnología informática.'},
            {'nombre': 'Desarrollo Personal', 'descripcion': 'Curso sobre desarrollo personal y habilidades blandas.'},
            {'nombre': 'Álgebra Vectorial', 'descripcion': 'Curso de álgebra vectorial aplicada.'},
            {'nombre': 'Matemática Discreta', 'descripcion': 'Curso sobre matemáticas discretas.'},
            {'nombre': 'Cálculo I', 'descripcion': 'Curso introductorio al cálculo.'},
            {'nombre': 'Fundamentos de Negocios', 'descripcion': 'Curso sobre los fundamentos básicos de los negocios.'},
            {'nombre': 'Teoría General de Sistemas', 'descripcion': 'Curso sobre la teoría general de sistemas.'},
            {'nombre': 'Algorítmica', 'descripcion': 'Curso sobre algoritmos y su aplicación.'},
            {'nombre': 'Física General', 'descripcion': 'Curso general de física aplicada.'},
            {'nombre': 'Organización y Arquitectura de Computadoras', 'descripcion': 'Curso sobre la organización y arquitectura de computadoras.'},
            {'nombre': 'Cálculo II', 'descripcion': 'Curso avanzado de cálculo.'},
            {'nombre': 'Gestión de Procesos', 'descripcion': 'Curso sobre la gestión de procesos empresariales.'},
            {'nombre': 'Estadística I', 'descripcion': 'Curso introductorio a la estadística.'},
            {'nombre': 'Pensamiento Sistémico', 'descripcion': 'Curso sobre el pensamiento sistémico.'},
            {'nombre': 'Estructura de Datos', 'descripcion': 'Curso sobre estructuras de datos y su aplicación.'},
            {'nombre': 'Fundamentos de Redes y Telecomunicaciones', 'descripcion': 'Curso sobre los fundamentos de telecomunicaciones.'},
            {'nombre': 'Sistemas Operativos', 'descripcion': 'Curso sobre sistemas operativos y su gestión.'},
            {'nombre': 'Cálculo III', 'descripcion': 'Curso avanzado de cálculo.'},
            {'nombre': 'Análisis y Diseño de Sistemas', 'descripcion': 'Curso sobre el análisis y diseño de sistemas informáticos.'},
            {'nombre': 'Estadística II', 'descripcion': 'Curso avanzado de estadística.'},
            {'nombre': 'Base de Datos I', 'descripcion': 'Curso sobre bases de datos relacionales.'},
            {'nombre': 'Programación Orientada a Objetos', 'descripcion': 'Curso sobre programación orientada a objetos.'},
            {'nombre': 'Redes y Telecomunicaciones I', 'descripcion': 'Curso sobre redes y telecomunicaciones.'},
            {'nombre': 'Servidores I', 'descripcion': 'Curso sobre la gestión de servidores.'},
            {'nombre': 'Desarrollo Web', 'descripcion': 'Curso sobre la creación de plataformas web.'},
            {'nombre': 'Ingeniería de Software', 'descripcion': 'Curso sobre los principios de la ingeniería de software.'},
            {'nombre': 'Fundamentos de Ciencia de Datos', 'descripcion': 'Curso sobre los fundamentos de la ciencia de datos.'},
            {'nombre': 'Base de Datos II', 'descripcion': 'Curso avanzado sobre bases de datos relacionales.'},
            {'nombre': 'Lenguaje de Programación I', 'descripcion': 'Curso sobre lenguaje de programación.'},
            {'nombre': 'Redes y Telecomunicaciones II', 'descripcion': 'Curso avanzado de redes y telecomunicaciones.'},
            {'nombre': 'Servidores II', 'descripcion': 'Curso avanzado sobre gestión de servidores.'},
            {'nombre': 'Experiencia de Usuario', 'descripcion': 'Curso sobre diseño de experiencia de usuario.'},
            {'nombre': 'Gestión de Proyectos I', 'descripcion': 'Curso sobre la gestión de proyectos empresariales.'},
            {'nombre': 'Metodología de la Investigación Científica', 'descripcion': 'Curso sobre métodos de investigación científica.'},
            {'nombre': 'Lenguaje de Programación II', 'descripcion': 'Curso avanzado de lenguaje de programación.'},
            {'nombre': 'Seguridad de la Información', 'descripcion': 'Curso sobre los principios de la seguridad de la información.'},
            {'nombre': 'Computación en la Nube', 'descripcion': 'Curso sobre tecnologías de computación en la nube.'},
            {'nombre': 'Inteligencia Artificial', 'descripcion': 'Curso introductorio a la inteligencia artificial.'},
            {'nombre': 'Gestión de Proyectos II', 'descripcion': 'Curso avanzado de gestión de proyectos.'},
            {'nombre': 'Seminario de Tesis I', 'descripcion': 'Curso de seminario para el desarrollo de tesis.'},
            {'nombre': 'Lenguaje de Programación III', 'descripcion': 'Curso avanzado de lenguaje de programación.'},
            {'nombre': 'Hacking Ético', 'descripcion': 'Curso sobre técnicas de hacking con fines éticos.'},
            {'nombre': 'Evaluación de Software', 'descripcion': 'Curso sobre evaluación y control de calidad del software.'},
            {'nombre': 'Inteligencia de Negocios', 'descripcion': 'Curso sobre inteligencia empresarial y análisis de datos.'},
            {'nombre': 'Ingeniería de la Información', 'descripcion': 'Curso sobre ingeniería y procesamiento de la información.'},
            {'nombre': 'Seminario de Tesis II', 'descripcion': 'Curso avanzado de seminario para tesis.'},
            {'nombre': 'Desarrollo de Aplicaciones Móviles', 'descripcion': 'Curso que aborda el diseño, desarrollo e implementación de aplicaciones móviles, incluyendo principios de usabilidad, arquitectura de aplicaciones y uso de frameworks para plataformas como Android e iOS.'},
            {'nombre': 'Derecho Informático y Ética Profesional', 'descripcion': 'Curso sobre derecho informático y ética profesional.'},
            {'nombre': 'Auditoría de Sistemas e Informática', 'descripcion': 'Curso sobre auditoría de sistemas informáticos.'},
            {'nombre': 'Internet de las Cosas', 'descripcion': 'Curso sobre la tecnología del Internet de las cosas.'},
            {'nombre': 'Formulación y Evaluación de Proyectos de Inversión', 'descripcion': 'Curso que enseña las técnicas y metodologías para la formulación, análisis y evaluación financiera de proyectos de inversión, con un enfoque en la toma de decisiones y la viabilidad económica.'},
            {'nombre': 'Seminario de Tesis III', 'descripcion': 'Curso final de seminario para la tesis.'},
            {'nombre': 'Gobierno de Tecnología de la Información', 'descripcion': 'Curso sobre la gestión y gobierno de TI.'}
        ]

        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                nombre=curso_data['nombre'],
                defaults={
                    'descripcion': curso_data['descripcion'],
                    'color': '#FFFFFF',  # Cambia esto por los colores que desees
                    'programa_academico': programa
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Curso {curso.nombre} creado"))
            else:
                self.stdout.write(self.style.WARNING(f"Curso {curso.nombre} ya existía"))

        # Crear íconos
        icon_path = 'static/icons/'

        iconos = [
            {'nombre': 'Book', 'imagen': 'book.svg'},
        ]

        for icono_data in iconos:
            icono, created = Icono.objects.get_or_create(nombre=icono_data['nombre'])
            if not icono.imagen:
                image_path = os.path.join(icon_path, icono_data['imagen'])
                with open(image_path, 'rb') as image_file:
                    icono.imagen.save(icono_data['imagen'], File(image_file), save=True)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Icono {icono.nombre} creado"))
            else:
                self.stdout.write(self.style.WARNING(f"Icono {icono.nombre} ya existía"))

        self.stdout.write(self.style.SUCCESS("Seed completado exitosamente."))
