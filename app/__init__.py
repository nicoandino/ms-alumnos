from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.settings.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app) 

    # Import models
    from app.models import Alumno, TipoDocumento
    
    # Import routes
    from app.routes.alumno_routes import alumno_bp
    from app.routes.tipodocumento_routes import tipodoc_bp

    app.register_blueprint(alumno_bp)
    app.register_blueprint(tipodoc_bp)

    # registrar blueprints
    return app
