from marshmallow import Schema, fields, post_load, validate
from app.models import Alumno

class AlumnoMapping(Schema):
    id = fields.Integer(dump_only=True)

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=100))

    nro_documento = fields.Integer(required=True)
    tipo_documento = fields.String(required=True, validate=validate.Length(min=1, max=10))

    sexo = fields.String(required=True, validate=validate.Length(equal=1))
    nro_legajo = fields.Integer(required=True)

    especialidad_id = fields.Integer(required=True)

    @post_load
    def nuevo_alumno(self, data, **kwargs):
        return Alumno(**data)
