from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tempsmart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Cambia esto a una clave secreta segura
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app.models import Usuario, Curso, TipoEvento, Evento, Notificacion, HorarioPersonalizado, CursoHorario
        db.create_all()

    # Inicializar rutas
    from .routes.usuarios import init_user_routes
    from app.routes.auth_routes import init_auth_routes
    init_user_routes(app)
    init_auth_routes(app)

    return app
