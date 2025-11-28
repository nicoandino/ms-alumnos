from flask import Blueprint, jsonify, request
from app import db
from app.models.tipodocumento import TipoDocumento
from app.schemas.tipodocumento_schema import tipodocumento_schema, tipodocumentos_schema

tipodoc_bp = Blueprint("tipodoc_bp", __name__)

@tipodoc_bp.get("/tipodocumentos")
def get_tipodocumentos():
    docs = TipoDocumento.query.all()
    return jsonify(tipodocumentos_schema.dump(docs)), 200

