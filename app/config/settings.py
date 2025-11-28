import os
from dotenv import load_dotenv

# Carga .env si existe; en Docker con --env-file funciona perfecto
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

def factory(env_name: str):
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestConfig,
    }
    return configs[env_name]
