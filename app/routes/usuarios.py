from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db
from app.models import Usuario

usuario_bp = Blueprint('usuarios', __name__)

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['rol'] != 'administrador':
            return jsonify({'error': 'No tienes permiso para acceder a este recurso'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@usuario_bp.route('/usuarios', methods=['GET'])
@admin_required
def obtener_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@admin_required
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.to_dict()), 200

@usuario_bp.route('/usuarios', methods=['POST'])
@admin_required
def agregar_usuario():
    datos = request.get_json()
    if not datos or not all(key in datos for key in ('nombre_usuario', 'correo_electronico', 'contrasena', 'nombre', 'apellido', 'rol', 'fecha_nacimiento')):
        return jsonify({'error': 'Datos inválidos'}), 400

    nuevo_usuario = Usuario(
        nombre_usuario=datos['nombre_usuario'],
        correo_electronico=datos['correo_electronico'],
        contrasena=generate_password_hash(datos['contrasena'], method='pbkdf2:sha256'),
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        rol=datos['rol'],
        fecha_nacimiento=datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d').date()
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_usuario(id):
    current_user = get_jwt_identity()
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar permisos
    if current_user['rol'] != 'administrador' and current_user['id'] != id:
        return jsonify({'error': 'No tienes permiso para acceder a este recurso'}), 403
    
    datos = request.get_json()
    if datos:
        if 'nombre_usuario' in datos:
            usuario.nombre_usuario = datos['nombre_usuario']
        if 'correo_electronico' in datos:
            usuario.correo_electronico = datos['correo_electronico']
        if 'contrasena' in datos:
            usuario.contrasena = generate_password_hash(datos['contrasena'], method='pbkdf2:sha256')
        if 'nombre' in datos:
            usuario.nombre = datos['nombre']
        if 'apellido' in datos:
            usuario.apellido = datos['apellido']
        if 'rol' in datos and current_user['rol'] == 'administrador':
            usuario.rol = datos['rol']
        if 'fecha_nacimiento' in datos:
            usuario.fecha_nacimiento = datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d').date()
        
        db.session.commit()
    return jsonify(usuario.to_dict()), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return 'Usuario eliminado', 204

@usuario_bp.route('/usuarios/me', methods=['PUT'])
@jwt_required()
def actualizar_mis_datos():
    current_user = get_jwt_identity()
    usuario = Usuario.query.get_or_404(current_user['id'])
    
    datos = request.get_json()
    if datos:
        if 'nombre_usuario' in datos:
            usuario.nombre_usuario = datos['nombre_usuario']
        if 'correo_electronico' in datos:
            usuario.correo_electronico = datos['correo_electronico']
        if 'contrasena' in datos:
            usuario.contrasena = generate_password_hash(datos['contrasena'], method='pbkdf2:sha256')
        if 'nombre' in datos:
            usuario.nombre = datos['nombre']
        if 'apellido' in datos:
            usuario.apellido = datos['apellido']
        if 'fecha_nacimiento' in datos:
            usuario.fecha_nacimiento = datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d').date()
        
        db.session.commit()
    return jsonify(usuario.to_dict()), 200

def init_user_routes(app):
    app.register_blueprint(usuario_bp)
