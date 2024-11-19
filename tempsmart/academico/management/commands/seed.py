from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from academico.models import ProgramaAcademico, PerfilUsuario, Curso, Icono, TipoHorario, Publicacion
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
            {'nombre': 'Lenguaje I', 'descripcion': 'Curso general sobre habilidades de lenguaje.', 'color': '#FF5733'},
            {'nombre': 'Matemática Básica I', 'descripcion': 'Curso introductorio de matemáticas básicas.', 'color': '#33FF57'},
            {'nombre': 'Métodos y Técnicas de Estudio', 'descripcion': 'Curso sobre métodos y técnicas para mejorar el estudio.', 'color': '#3357FF'},
            {'nombre': 'Psicología General', 'descripcion': 'Curso introductorio a la psicología.', 'color': '#FF33A6'},
            {'nombre': 'Introducción a la Ingeniería de Sistemas e Informática', 'descripcion': 'Curso introductorio a la ingeniería de sistemas.', 'color': '#FF8C33'},
            {'nombre': 'Ética y Liderazgo', 'descripcion': 'Curso sobre principios éticos y liderazgo.', 'color': '#33FFF5'},
            {'nombre': 'Lenguaje II', 'descripcion': 'Curso avanzado sobre habilidades de lenguaje.', 'color': '#B833FF'},
            {'nombre': 'Matemática Básica II', 'descripcion': 'Curso avanzado de matemáticas básicas.', 'color': '#FF3366'},
            {'nombre': 'Ecología y Protección del Medio Ambiente', 'descripcion': 'Curso sobre ecología y protección ambiental.', 'color': '#33FFB2'},
            {'nombre': 'Sociología General', 'descripcion': 'Curso introductorio a la sociología.', 'color': '#FFD633'},
            {'nombre': 'Tecnología Informática', 'descripcion': 'Curso sobre el uso de tecnología informática.', 'color': '#33D4FF'},
            {'nombre': 'Desarrollo Personal', 'descripcion': 'Curso sobre desarrollo personal y habilidades blandas.', 'color': '#8CFF33'},
            {'nombre': 'Álgebra Vectorial', 'descripcion': 'Curso de álgebra vectorial aplicada.', 'color': '#FF5733'},
            {'nombre': 'Matemática Discreta', 'descripcion': 'Curso sobre matemáticas discretas.', 'color': '#33FFC1'},
            {'nombre': 'Cálculo I', 'descripcion': 'Curso introductorio al cálculo.', 'color': '#337BFF'},
            {'nombre': 'Fundamentos de Negocios', 'descripcion': 'Curso sobre los fundamentos básicos de los negocios.', 'color': '#FF334D'},
            {'nombre': 'Teoría General de Sistemas', 'descripcion': 'Curso sobre la teoría general de sistemas.', 'color': '#FFB833'},
            {'nombre': 'Algorítmica', 'descripcion': 'Curso sobre algoritmos y su aplicación.', 'color': '#33FF83'},
            {'nombre': 'Física General', 'descripcion': 'Curso general de física aplicada.', 'color': '#A333FF'},
            {'nombre': 'Organización y Arquitectura de Computadoras', 'descripcion': 'Curso sobre la organización y arquitectura de computadoras.', 'color': '#33FF57'},
            {'nombre': 'Cálculo II', 'descripcion': 'Curso avanzado de cálculo.', 'color': '#FF335C'},
            {'nombre': 'Gestión de Procesos', 'descripcion': 'Curso sobre la gestión de procesos empresariales.', 'color': '#33FFA8'},
            {'nombre': 'Estadística I', 'descripcion': 'Curso introductorio a la estadística.', 'color': '#FFC133'},
            {'nombre': 'Pensamiento Sistémico', 'descripcion': 'Curso sobre el pensamiento sistémico.', 'color': '#33D7FF'},
            {'nombre': 'Estructura de Datos', 'descripcion': 'Curso sobre estructuras de datos y su aplicación.', 'color': '#63FF33'},
            {'nombre': 'Fundamentos de Redes y Telecomunicaciones', 'descripcion': 'Curso sobre los fundamentos de telecomunicaciones.', 'color': '#FF5733'},
            {'nombre': 'Sistemas Operativos', 'descripcion': 'Curso sobre sistemas operativos y su gestión.', 'color': '#33FFF2'},
            {'nombre': 'Cálculo III', 'descripcion': 'Curso avanzado de cálculo.', 'color': '#335BFF'},
            {'nombre': 'Análisis y Diseño de Sistemas', 'descripcion': 'Curso sobre el análisis y diseño de sistemas informáticos.', 'color': '#FF33A8'},
            {'nombre': 'Estadística II', 'descripcion': 'Curso avanzado de estadística.', 'color': '#FF9633'},
            {'nombre': 'Base de Datos I', 'descripcion': 'Curso sobre bases de datos relacionales.', 'color': '#FF5733'},
            {'nombre': 'Programación Orientada a Objetos', 'descripcion': 'Curso sobre programación orientada a objetos.', 'color': '#33FF57'},
            {'nombre': 'Redes y Telecomunicaciones I', 'descripcion': 'Curso sobre redes y telecomunicaciones.', 'color': '#FF33A6'},
            {'nombre': 'Servidores I', 'descripcion': 'Curso sobre la gestión de servidores.', 'color': '#FF8C33'},
            {'nombre': 'Desarrollo Web', 'descripcion': 'Curso sobre la creación de plataformas web.', 'color': '#33FFF5'},
            {'nombre': 'Ingeniería de Software', 'descripcion': 'Curso sobre los principios de la ingeniería de software.', 'color': '#B833FF'},
            {'nombre': 'Fundamentos de Ciencia de Datos', 'descripcion': 'Curso sobre los fundamentos de la ciencia de datos.', 'color': '#FF3366'},
            {'nombre': 'Base de Datos II', 'descripcion': 'Curso avanzado sobre bases de datos relacionales.', 'color': '#33FFB2'},
            {'nombre': 'Lenguaje de Programación I', 'descripcion': 'Curso sobre lenguaje de programación.', 'color': '#FFD633'},
            {'nombre': 'Redes y Telecomunicaciones II', 'descripcion': 'Curso avanzado de redes y telecomunicaciones.', 'color': '#33D4FF'},
            {'nombre': 'Servidores II', 'descripcion': 'Curso avanzado sobre gestión de servidores.', 'color': '#8CFF33'},
            {'nombre': 'Experiencia de Usuario', 'descripcion': 'Curso sobre diseño de experiencia de usuario.', 'color': '#FF5733'},
            {'nombre': 'Gestión de Proyectos I', 'descripcion': 'Curso sobre la gestión de proyectos empresariales.', 'color': '#33FFC1'},
            {'nombre': 'Metodología de la Investigación Científica', 'descripcion': 'Curso sobre métodos de investigación científica.', 'color': '#337BFF'},
            {'nombre': 'Lenguaje de Programación II', 'descripcion': 'Curso avanzado de lenguaje de programación.', 'color': '#FF334D'},
            {'nombre': 'Seguridad de la Información', 'descripcion': 'Curso sobre los principios de la seguridad de la información.', 'color': '#FFB833'},
            {'nombre': 'Computación en la Nube', 'descripcion': 'Curso sobre tecnologías de computación en la nube.', 'color': '#33FF83'},
            {'nombre': 'Inteligencia Artificial', 'descripcion': 'Curso introductorio a la inteligencia artificial.', 'color': '#A333FF'},
            {'nombre': 'Gestión de Proyectos II', 'descripcion': 'Curso avanzado de gestión de proyectos.', 'color': '#33FF57'},
            {'nombre': 'Seminario de Tesis I', 'descripcion': 'Curso de seminario para el desarrollo de tesis.', 'color': '#FF335C'},
            {'nombre': 'Lenguaje de Programación III', 'descripcion': 'Curso avanzado de lenguaje de programación.', 'color': '#33FFA8'},
            {'nombre': 'Hacking Ético', 'descripcion': 'Curso sobre técnicas de hacking con fines éticos.', 'color': '#FFC133'},
            {'nombre': 'Evaluación de Software', 'descripcion': 'Curso sobre evaluación y control de calidad del software.', 'color': '#33D7FF'},
            {'nombre': 'Inteligencia de Negocios', 'descripcion': 'Curso sobre inteligencia empresarial y análisis de datos.', 'color': '#63FF33'},
            {'nombre': 'Ingeniería de la Información', 'descripcion': 'Curso sobre ingeniería y procesamiento de la información.', 'color': '#FF5733'},
            {'nombre': 'Seminario de Tesis II', 'descripcion': 'Curso avanzado de seminario para tesis.', 'color': '#33FFF2'},
            {'nombre': 'Desarrollo de Aplicaciones Móviles', 'descripcion': 'Curso sobre el diseño y desarrollo de aplicaciones móviles.', 'color': '#335BFF'},
            {'nombre': 'Derecho Informático y Ética Profesional', 'descripcion': 'Curso sobre derecho informático y ética profesional.', 'color': '#FF33A8'},
            {'nombre': 'Auditoría de Sistemas e Informática', 'descripcion': 'Curso sobre auditoría de sistemas informáticos.', 'color': '#FF9633'},
            {'nombre': 'Internet de las Cosas', 'descripcion': 'Curso sobre la tecnología del Internet de las cosas.', 'color': '#FF5733'},
            {'nombre': 'Formulación y Evaluación de Proyectos de Inversión', 'descripcion': 'Curso sobre formulación de proyectos de inversión.', 'color': '#33FF57'},
            {'nombre': 'Seminario de Tesis III', 'descripcion': 'Curso final de seminario para la tesis.', 'color': '#FF33A6'},
            {'nombre': 'Gobierno de Tecnología de la Información', 'descripcion': 'Curso sobre la gestión y gobierno de TI.', 'color': '#FF8C33'}
        ]

        cursos = {}

        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                nombre=curso_data['nombre'],
                defaults={
                    'descripcion': curso_data['descripcion'],
                    'color': curso_data['color'],
                    'programa_academico': programa
                }
            )
            cursos[curso_data['nombre']] = curso
            if created:
                self.stdout.write(self.style.SUCCESS(f"Curso {curso.nombre} creado"))
            else:
                self.stdout.write(self.style.WARNING(f"Curso {curso.nombre} ya existía"))

        # Crear íconos
        iconos = [
            {'nombre': 'Clase', 'imagen': 'ClassIcon'},
            {'nombre': 'Laptop', 'imagen': 'LaptopIcon'},
            {'nombre': 'Bolígrafo', 'imagen': 'EditIcon'},
            {'nombre': 'Alarma', 'imagen': 'AccessAlarmIcon'},
            {'nombre': 'Libro', 'imagen': 'MenuBookIcon'},
            {'nombre': 'Mensaje', 'imagen': 'MailOutlineIcon'},
            {'nombre': 'Marcador', 'imagen': 'BookmarkIcon'},
            {'nombre': 'Favorito', 'imagen': 'StarIcon'},
            {'nombre': 'Importante', 'imagen': 'CrisisAlertIcon'},
            {'nombre': 'Reunion', 'imagen': 'GroupsIcon'},
        ]

        for icono_data in iconos:
            icono, created = Icono.objects.get_or_create(
                nombre=icono_data['nombre'],
                defaults={'imagen': icono_data['imagen']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Icono {icono.nombre} creado con referencia {icono.imagen}"))
            else:
                self.stdout.write(self.style.WARNING(f"Icono {icono.nombre} ya existía con referencia {icono.imagen}"))

        # Crear publicaciones con apuntes académicos
        publicaciones_data = [
            {
                'curso': cursos['Lenguaje I'],
                'titulo': 'Apuntes sobre análisis de textos literarios',
                'contenido': """
**Temas tratados:**
1. Introducción a los géneros literarios (narrativo, lírico, dramático).
2. Análisis de textos argumentativos.
3. Uso de conectores y cohesión textual.

**Palabras clave principales:**
- Géneros literarios
- Análisis crítico
- Cohesión y coherencia

**Posibles preguntas de examen:**
1. ¿Cuáles son las características principales de un texto narrativo?
2. Enumera y explica los tipos de conectores utilizados en un texto argumentativo.
3. Realiza un análisis crítico de un texto lírico.

""",
            },
            {
                'curso': cursos['Matemática Básica I'],
                'titulo': 'Apuntes sobre álgebra básica',
                'contenido': """
**Temas tratados:**
1. Operaciones básicas con números enteros y fracciones.
2. Resolución de ecuaciones lineales.
3. Propiedades de los números primos.

**Palabras clave principales:**
- Ecuaciones lineales
- Fracciones
- Números primos

**Posibles preguntas de examen:**
1. Resuelve la ecuación: 2x + 5 = 15.
2. ¿Cuáles son las propiedades fundamentales de los números primos?
3. Simplifica: (3/4) + (5/6).
""",
            },
            {
                'curso': cursos['Psicología General'],
                'titulo': 'Apuntes sobre teoría del aprendizaje',
                'contenido': """
**Temas tratados:**
1. Teoría conductista: Pavlov y Skinner.
2. Teoría cognitiva: Piaget.
3. Aprendizaje social: Bandura.

**Palabras clave principales:**
- Conductismo
- Desarrollo cognitivo
- Aprendizaje social

**Posibles preguntas de examen:**
1. ¿Cuál es la diferencia entre refuerzo positivo y negativo en el conductismo?
2. Explica las etapas del desarrollo cognitivo según Piaget.
3. ¿Qué se entiende por aprendizaje vicario según Bandura?
""",
            },
            {
                'curso': cursos['Introducción a la Ingeniería de Sistemas e Informática'],
                'titulo': 'Apuntes sobre conceptos básicos de sistemas',
                'contenido': """
**Temas tratados:**
1. Definición de sistemas y componentes principales.
2. Ciclo de vida de un sistema.
3. Introducción a los sistemas de información.

**Palabras clave principales:**
- Sistema
- Ciclo de vida
- Sistemas de información

**Posibles preguntas de examen:**
1. Define qué es un sistema y menciona sus componentes básicos.
2. ¿Qué etapas componen el ciclo de vida de un sistema?
3. ¿Cuál es la diferencia entre datos e información en un sistema informático?
""",
            },
            {
                'curso': cursos['Ética y Liderazgo'],
                'titulo': 'Apuntes sobre principios éticos en el liderazgo',
                'contenido': """
**Temas tratados:**
1. Concepto de ética profesional.
2. Liderazgo transformacional y situacional.
3. Toma de decisiones éticas en el trabajo.

**Palabras clave principales:**
- Ética profesional
- Liderazgo transformacional
- Toma de decisiones

**Posibles preguntas de examen:**
1. Explica qué es la ética profesional y su importancia en el liderazgo.
2. Diferencia entre liderazgo transformacional y situacional.
3. Describe un caso práctico de toma de decisiones éticas.
""",
            },
        ]

        for publicacion_data in publicaciones_data:
            publicacion, created = Publicacion.objects.get_or_create(
                curso=publicacion_data['curso'],
                titulo=publicacion_data['titulo'],
                defaults={
                    'contenido': publicacion_data['contenido']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Publicación '{publicacion.titulo}' creada"))
            else:
                self.stdout.write(self.style.WARNING(f"Publicación '{publicacion.titulo}' ya existía"))

        self.stdout.write(self.style.SUCCESS("Seed completado exitosamente."))