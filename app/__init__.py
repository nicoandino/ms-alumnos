from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.settings.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Alumno, TipoDocumento
    
    # registrar blueprints
    return app
