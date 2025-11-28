from app import ma
from app.models.alumno import Alumno

class AlumnoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alumno
        load_instance = True

alumno_schema = AlumnoSchema()
alumnos_schema = AlumnoSchema(many=True)
