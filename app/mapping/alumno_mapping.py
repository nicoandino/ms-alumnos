from marshmallow import Schema, fields, post_load, validate, ValidationError
from app.models import Alumno, TipoDocumento

class AlumnoMapping(Schema):
    id = fields.Integer(dump_only=True)

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=100))

    nro_documento = fields.Integer(required=True)
    tipo_documento = fields.Function(
        serialize=lambda obj: obj.tipo_documento.sigla if obj.tipo_documento else None,
        deserialize=lambda value: value,
        required=True
    )

    sexo = fields.String(required=True, validate=validate.Length(equal=1))
    nro_legajo = fields.Integer(required=True)

    especialidad_id = fields.Integer(required=True)

    @post_load
    def nuevo_alumno(self, data, **kwargs):
        # data['tipo_documento'] es la sigla que vino en el JSON
        sigla = data.pop("tipo_documento", None)
        if not sigla:
            raise ValidationError({"tipo_documento": "Este campo es obligatorio."})

        tipo = TipoDocumento.query.filter_by(sigla=sigla).first()
        if not tipo:
            raise ValidationError({"tipo_documento": f"Tipo de documento '{sigla}' inválido."})

        data["tipo_documento_id"] = tipo.id

        return Alumno(**data)
