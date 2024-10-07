import re

def extract_courses_info(text):
    """
    Extrae la información de los cursos del PDF, capturando todos los cursos, incluidos aquellos que tienen estructuras fragmentadas.
    """
    # Patrón para capturar cursos con sus códigos, nombres, ciclo, y créditos
    # Ajustamos el patrón para capturar también cursos fragmentados
    curso_pattern = re.compile(r'(\d{9})\s+([A-ZÁÉÍÓÚÑ ]+(?:\s[A-ZÁÉÍÓÚÑ ]+)*)\s+(\d+)\s+(\d+)\s+[A]')
    
    # Patrón para capturar los docentes
    docente_pattern = re.compile(r'Docente\s([A-ZÁÉÍÓÚÑ ]+)(?:\n)?([A-ZÁÉÍÓÚÑ ]*)')

    # Lista de colores bonitos
    colores_bonitos = [
        "#FF5733",  # Rojo anaranjado
        "#33FF57",  # Verde brillante
        "#3357FF",  # Azul fuerte
        "#FF33A6",  # Rosa brillante
        "#33FFF5",  # Turquesa claro
        "#FFC300",  # Amarillo cálido
        "#DAF7A6",  # Verde pastel
    ]

    cursos_info = []
    # Encontrar todos los cursos
    cursos_matches = curso_pattern.findall(text)

    # Encontrar todos los docentes
    docente_matches = docente_pattern.findall(text)

    # Proceso de detección de cursos con horarios fragmentados
    # Este patrón busca casos como el de "Marketing Digital"
    curso_fragmentado_pattern = re.compile(r'(\d{9})\s+([A-ZÁÉÍÓÚÑ ]+)\s+(\d+)\s+(\d+)\s+[A]')

    fragment_matches = curso_fragmentado_pattern.findall(text)

    # Combina ambos conjuntos de matches en una sola lista de cursos encontrados
    cursos_totales = cursos_matches + fragment_matches

    # Iterar sobre los cursos encontrados
    for i, match in enumerate(cursos_totales):
        codigo_curso, nombre_curso, ciclo, creditos = match
        nombre_curso = " ".join(nombre_curso.split())  # Limpiar el nombre del curso

        # Asignar el docente correspondiente si está disponible
        docente = " ".join([part for part in docente_matches[i] if part]).strip() if i < len(docente_matches) else "Docente desconocido"

        # Asignar un color bonito diferente para cada curso (cíclico si hay más de 7 cursos)
        color = colores_bonitos[i % len(colores_bonitos)]

        curso_data = {
            'codigo': codigo_curso,
            'nombre': nombre_curso,
            'docente': docente,
            'color': color,
            'horarios': []  # Los horarios los procesaremos después
        }

        cursos_info.append(curso_data)

    return cursos_info

def convertir_dia_a_numero(dia):
    """
    Convierte el día de la semana en un número (Lunes=1, Domingo=7).
    """
    dias_semana = {
        'Lunes': 1,
        'Martes': 2,
        'Miércoles': 3,
        'Jueves': 4,
        'Viernes': 5,
        'Sábado': 6,
        'Domingo': 7
    }
    return dias_semana.get(dia, None)
