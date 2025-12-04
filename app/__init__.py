import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app() -> Flask:
    app = Flask(__name__)

    # Contexto de la app: viene del .env del contenedor (docker/.env)
    # Ejemplos: FLASK_CONTEXT=development | testing | production
    flask_context = os.getenv("FLASK_CONTEXT", "development").lower()
    app.config["DEBUG"] = flask_context == "development"
    app.config["TESTING"] = flask_context == "testing"

    # Datos de la base (también vienen del .env del contenedor)
    db_host = os.getenv("HOST_DB", "localhost")
    db_user = os.getenv("USER_DB", "postgres")
    db_password = os.getenv("PASSWORD_DB", "")
    db_name = os.getenv("NAME_DB", "postgres")

    uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)

    # Registrar blueprints
    from app.resources import home, alumno_bp
    app.register_blueprint(home)
    app.register_blueprint(alumno_bp, url_prefix="/api/v1/alumno")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
