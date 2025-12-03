from dataclasses import dataclass
from datetime import date
from app.models.tipodocumento import TipoDocumento
from app import db

@dataclass(init=False, repr=True, eq=True)
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id:int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre:str = db.Column(db.String(50), nullable=False) 
    apellido:str = db.Column(db.String(50), nullable=False)
    nrodocumento: str= db.Column(db.String(50), nullable=False)

    tipo_documento_id:int = db.Column(db.Integer, db.ForeignKey('tipodocumentos.id'), nullable=False)
    tipo_documento = db.relationship('TipoDocumento',  lazy=True)

    fecha_nacimiento:date = db.Column(db.Date, nullable=False)
    sexo:str = db.Column(db.String(1), nullable=False) 
    nro_legajo:int = db.Column(db.Integer, nullable=False)
    fecha_ingreso:date = db.Column(db.Date, nullable=False) 

    