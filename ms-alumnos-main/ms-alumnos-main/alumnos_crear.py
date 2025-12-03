# alumnos_crear.py
from datetime import date
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models.alumno import Alumno
from app.models.tipodocumento import TipoDocumento
from app import db

#DATABASE_URI = "postgresql+psycopg2://postgres:sucontraseña@localhost:5432/test_sysacad"
DATABASE_URI = "postgresql+psycopg2://postgres:nico@localhost:5432/test_sysacad"

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# ============================================================
# 1. CREAR SOLO LAS TABLAS NECESARIAS PARA EL MS
# ============================================================

with engine.connect() as conn:
    print("🔧 Creando tablas necesarias...")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tipodocumentos (
            id SERIAL PRIMARY KEY,
            sigla VARCHAR(10) NOT NULL,
            nombre VARCHAR(50) NOT NULL
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            nrodocumento VARCHAR(50) NOT NULL,
            tipo_documento_id INTEGER NOT NULL REFERENCES tipodocumentos(id),
            fecha_nacimiento DATE NOT NULL,
            sexo VARCHAR(1) NOT NULL,
            nro_legajo INTEGER NOT NULL,
            fecha_ingreso DATE NOT NULL
        );
    """))

    conn.commit()

print("   ✓ Tablas creadas correctamente\n")

# ============================================================
# 2. TIPOS DE DOCUMENTO
# ============================================================
dni = session.query(TipoDocumento).filter_by(sigla="DNI").first()
pas = session.query(TipoDocumento).filter_by(sigla="PAS").first()

if not dni:
    dni = TipoDocumento(sigla="DNI", nombre="Documento Nacional de Identidad")
    session.add(dni)

if not pas:
    pas = TipoDocumento(sigla="PAS", nombre="Pasaporte")
    session.add(pas)

session.commit()

print(f"📄 TiposDocumento: DNI={dni.id}, PAS={pas.id}\n")

# ============================================================
# 3. INSERTAR 5 ALUMNOS
# ============================================================
print("👨‍🎓 Insertando alumnos...")

alumnos = [
    Alumno(
        nombre="Pepito",
        apellido="Flores",
        nrodocumento="40123456",
        tipo_documento_id=dni.id,
        fecha_nacimiento=date(2002, 3, 15),
        sexo="M",
        nro_legajo=1001,
        fecha_ingreso=date(2021, 2, 1)
    ),
    Alumno(
        nombre="Camila",
        apellido="Sosa",
        nrodocumento="37888999",
        tipo_documento_id=dni.id,
        fecha_nacimiento=date(2001, 7, 20),
        sexo="F",
        nro_legajo=1002,
        fecha_ingreso=date(2021, 3, 10)
    ),
    Alumno(
        nombre="Matías",
        apellido="Gómez",
        nrodocumento="41222333",
        tipo_documento_id=pas.id,
        fecha_nacimiento=date(2000, 10, 1),
        sexo="M",
        nro_legajo=1003,
        fecha_ingreso=date(2020, 8, 20)
    ),
    Alumno(
        nombre="Lucía",
        apellido="Martínez",
        nrodocumento="40222111",
        tipo_documento_id=dni.id,
        fecha_nacimiento=date(2003, 4, 11),
        sexo="F",
        nro_legajo=1004,
        fecha_ingreso=date(2022, 1, 5)
    ),
    Alumno(
        nombre="Bruno",
        apellido="Fernández",
        nrodocumento="35555777",
        tipo_documento_id=pas.id,
        fecha_nacimiento=date(1999, 9, 27),
        sexo="M",
        nro_legajo=1005,
        fecha_ingreso=date(2019, 9, 1)
    )
]

session.add_all(alumnos)
session.commit()

print("🎉 5 alumnos insertados correctamente en test_sysacad")
