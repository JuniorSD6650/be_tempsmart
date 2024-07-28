from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activities.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.activity_routes import init_activity_routes
    from app.routes.user_routes import init_user_routes

    init_activity_routes(app)
    init_user_routes(app)

    return app
