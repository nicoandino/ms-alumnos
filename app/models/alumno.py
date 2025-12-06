from dataclasses import dataclass
from app import db

@dataclass
class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nombre: str = db.Column(db.String(100), nullable=False)
    apellido: str = db.Column(db.String(100), nullable=False)

    nro_documento: int = db.Column(db.Integer, nullable=False)

    tipo_documento_id: int = db.Column(db.Integer,db.ForeignKey('tipo_documento.id'),nullable=False)    
    tipo_documento = db.relationship('TipoDocumento', lazy=True)

    sexo: str = db.Column(db.String(1), nullable=False)
    nro_legajo: int = db.Column(db.Integer, nullable=False)

    especialidad_id: int = db.Column(db.Integer, nullable=False)
