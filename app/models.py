from . import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='estudiante')
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    cursos = db.relationship('Curso', backref='usuario', lazy=True)
    horarios_personalizados = db.relationship('HorarioPersonalizado', backref='usuario', lazy=True)
    __table_args__ = (
        db.UniqueConstraint('nombre_usuario', 'correo_electronico', name='unique_user_email'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'correo_electronico': self.correo_electronico,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rol': self.rol,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d')
        }

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    color = db.Column(db.String(7), nullable=True)  # For example, "#FF5733"
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ciclo = db.Column(db.String(5), nullable=False)  # Example values: "I", "II", ..., "X", "XI"
    nombre_profesor = db.Column(db.String(80), nullable=True)  # Optional field
    eventos = db.relationship('Evento', backref='curso', lazy=True)
    curso_horarios = db.relationship('CursoHorario', backref='curso', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'color': self.color,
            'ciclo': self.ciclo,
            'nombre_profesor': self.nombre_profesor
        }

class TipoEvento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    eventos = db.relationship('Evento', backref='tipo_evento', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.Integer, nullable=True)  # Duración en minutos, aplicable para exámenes
    icono = db.Column(db.String(200), nullable=True)  # Path or URL to custom icon
    estado = db.Column(db.String(20), nullable=False)  # Example values: "incompleto", "en avance", "completado"
    tipo_evento_id = db.Column(db.Integer, db.ForeignKey('tipo_evento.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_evento': self.fecha_evento.strftime('%Y-%m-%d %H:%M:%S'),
            'duracion': self.duracion,
            'icono': self.icono,
            'estado': self.estado,
            'tipo_evento_id': self.tipo_evento_id,
            'curso_id': self.curso_id
        }

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_notificacion = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'mensaje': self.mensaje,
            'fecha_notificacion': self.fecha_notificacion.strftime('%Y-%m-%d %H:%M:%S'),
            'usuario_id': self.usuario_id,
            'evento_id': self.evento_id
        }

class HorarioPersonalizado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cursos = db.relationship('CursoHorario', backref='horario_personalizado', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

class CursoHorario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario_personalizado_id = db.Column(db.Integer, db.ForeignKey('horario_personalizado.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 1: Monday, 2: Tuesday, ..., 7: Sunday
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    aula = db.Column(db.String(80), nullable=True)  # Optional field

    def to_dict(self):
        return {
            'id': self.id,
            'horario_personalizado_id': self.horario_personalizado_id,
            'curso_id': self.curso_id,
            'dia_semana': self.dia_semana,
            'hora_inicio': self.hora_inicio.strftime('%H:%M:%S'),
            'hora_fin': self.hora_fin.strftime('%H:%M:%S'),
            'aula': self.aula
        }
