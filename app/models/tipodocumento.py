from dataclasses import dataclass
from app import db

@dataclass(init=False)
class TipoDocumento(db.Model):
    __tablename__ = "tipo_documento"

    id: int
    sigla: str
    nombre: str

    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
