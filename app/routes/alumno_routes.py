from flask import Blueprint, request, jsonify
from app import db
from app.models.alumno import Alumno
from app.schemas.alumno_schema import alumno_schema, alumnos_schema

alumno_bp = Blueprint("alumno_bp", __name__)

# GET /alumnos (listar todos)
@alumno_bp.get("/alumnos")
def get_alumnos():
    alumnos = Alumno.query.all()
    return jsonify(alumnos_schema.dump(alumnos)), 200

# GET /alumnos/<id>
@alumno_bp.get("/alumnos/<int:id>")
def get_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    return alumno_schema.dump(alumno), 200

# POST /alumnos (crear)
@alumno_bp.post("/alumnos")
def create_alumno():
    data = request.json
    alumno = alumno_schema.load(data)
    db.session.add(alumno)
    db.session.commit()
    return alumno_schema.dump(alumno), 201

# PUT /alumnos/<id>
@alumno_bp.put("/alumnos/<int:id>")
def update_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    data = request.json

    for key, value in data.items():
        setattr(alumno, key, value)

    db.session.commit()
    return alumno_schema.dump(alumno), 200

# DELETE /alumnos/<id>
@alumno_bp.delete("/alumnos/<int:id>")
def delete_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return "", 204
