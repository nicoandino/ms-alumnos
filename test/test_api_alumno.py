import os
import unittest

os.environ["FLASK_CONTEXT"] = "testing"
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from datetime import date
from app import create_app, db
from app.models.tipodocumento import TipoDocumento


class AlumnoApiTestCase(unittest.TestCase):

    def setUp(self):
        # Eliminar las líneas de os.environ de aquí
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Datos base
        tipo_doc = TipoDocumento(sigla="DNI", nombre="Documento Nacional")
        db.session.add(tipo_doc)
        db.session.commit()
        self.tipo_doc_id = tipo_doc.id
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_listado_vacio(self):
        resp = self.client.get("/api/v1/alumno/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_crud_alumno(self):
        payload = {
            "nombre": "Juan",
            "apellido": "Perez",
            "nrodocumento": "12345678",
            "tipo_documento_id": self.tipo_doc_id,
            "fecha_nacimiento": "1990-01-01",
            "sexo": "M",
            "nro_legajo": 111,
            "fecha_ingreso": "2020-01-01"
        }

        # Crear
        resp = self.client.post("/api/v1/alumno/", json=payload)
        self.assertEqual(resp.status_code, 200)

        # Listar con un elemento
        resp_list = self.client.get("/api/v1/alumno/")
        self.assertEqual(resp_list.status_code, 200)
        alumnos = resp_list.get_json()
        self.assertEqual(len(alumnos), 1)
        alumno_id = alumnos[0]["id"]

        # Obtener por id
        resp_get = self.client.get(f"/api/v1/alumno/{alumno_id}")
        self.assertEqual(resp_get.status_code, 200)
        data = resp_get.get_json()
        self.assertEqual(data["nombre"], "Juan")

        # Actualizar
        payload_update = payload | {"nombre": "Juan Mod"}
        resp_put = self.client.put(f"/api/v1/alumno/{alumno_id}", json=payload_update)
        self.assertEqual(resp_put.status_code, 200)

        resp_get2 = self.client.get(f"/api/v1/alumno/{alumno_id}")
        self.assertEqual(resp_get2.get_json()["nombre"], "Juan Mod")

        # Borrar
        resp_del = self.client.delete(f"/api/v1/alumno/{alumno_id}")
        self.assertEqual(resp_del.status_code, 200)

        # Luego ya no debería encontrarlo (contrato actual devuelve 200 y None)
        resp_get3 = self.client.get(f"/api/v1/alumno/{alumno_id}")
        self.assertEqual(resp_get3.status_code, 200)
        self.assertEqual(resp_get3.get_json(), {})

    def test_payload_invalido(self):
        # Falta nombre, apellido, etc.
        resp = self.client.post("/api/v1/alumno/", json={})
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
