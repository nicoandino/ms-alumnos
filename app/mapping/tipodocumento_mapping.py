from marshmallow import fields, Schema, post_load, validate
from app.models import TipoDocumento

class TipoDocumentoMapping(Schema):
    id = fields.Integer(dump_only=True)
    sigla = fields.String(required=True, validate=validate.Length(min=1, max=10))
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))

    @post_load
    def nueva_tipodocumento(self, data, **kwargs):
        return TipoDocumento(**data)
