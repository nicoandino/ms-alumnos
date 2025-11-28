from app import ma
from app.models.tipodocumento import TipoDocumento

class TipoDocumentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoDocumento
        load_instance = True

tipodocumento_schema = TipoDocumentoSchema()
tipodocumentos_schema = TipoDocumentoSchema(many=True)
