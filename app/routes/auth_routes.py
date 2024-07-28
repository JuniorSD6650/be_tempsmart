from datetime import datetime
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    from app.models import Usuario
    data = request.get_json()
    if not data or not 'nombre_usuario' in data or not 'correo_electronico' in data or not 'contrasena' in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    hashed_password = generate_password_hash(data['contrasena'], method='pbkdf2:sha256')
    fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()

    nuevo_usuario = Usuario(
        nombre_usuario=data['nombre_usuario'],
        correo_electronico=data['correo_electronico'],
        contrasena=hashed_password,
        nombre=data['nombre'],
        apellido=data['apellido'],
        fecha_nacimiento=fecha_nacimiento
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from app.models import Usuario
    data = request.get_json()
    if not data or not 'correo_electronico' in data or not 'contrasena' in data:
        return jsonify({'error': 'Datos inválidos'}), 400
    usuario = Usuario.query.filter_by(correo_electronico=data['correo_electronico']).first()
    if not usuario or not check_password_hash(usuario.contrasena, data['contrasena']):
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401
    access_token = create_access_token(identity={'id': usuario.id, 'correo_electronico': usuario.correo_electronico, 'rol': usuario.rol})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Aquí puedes implementar el logout invalidando el token actual si guardas una lista de tokens válidos en la base de datos.
    return jsonify({'mensaje': 'Sesión cerrada correctamente'}), 200

def init_auth_routes(app):
    app.register_blueprint(auth_bp)
