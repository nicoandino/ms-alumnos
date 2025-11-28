import logging
import os
from flask import Flask
from app.config.settings import factory
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
ma = Marshmallow()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app_context = os.getenv('FLASK_CONTEXT')
    # https://flask.palletsprojects.com/en/stable/api/#flask.Flask
    app = Flask(__name__)
    f = factory(app_context if app_context else 'development')
    app.config.from_object(f)
    
    db.init_app(app)
    ma.init_app(app)
    
    from app.resources import home, alumno_bp
    app.register_blueprint(alumno_bp, url_prefix='/api/v1/alumno')
    app.register_blueprint(home, url_prefix='/api/v1')

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
