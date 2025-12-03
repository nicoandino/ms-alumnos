from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class TipoDocumento(db.Model):
    __tablename__ = 'tipodocumentos'

    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.Integer)
    libreta_civica = db.Column(db.String(20))
    libreta_enrolamiento = db.Column(db.String(20))
    pasaporte = db.Column(db.String(20))  # <---- AÑADIR
