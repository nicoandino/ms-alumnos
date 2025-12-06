
Microservicio realizado por los alumnos:
-Andino Nicolás , Legajo N°9935
-Assenza Ezequiel , Legajo N° 9943
-Lopez Matias , Legajo N° 10097 
-Orella Lucas , Legajo N° 10163

# uv

# Instalación
1. Abrir **consola de PowerShell como administrador**.  
2. Instalar `uv`:
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
3. Reiniciar la PC.

# Crear Proyecto
uv init nombre-proyecto
uv init  # si el proyecto ya existe

En nuestro caso ya existe, porque estarían copiando la carpeta desde Git.

# Instalación de entorno virtual (venv)
uv venv

# Agregar dependencias 
uv add flask==3.1.2

# Sincronizar dependencias 
uv sync

# Documentación
Referencia: https://docs.astral.sh/uv/getting-started/first-steps/


# Granian

Servidor HTTP de **alto rendimiento** escrito en **Rust** para **aplicaciones Python**.  
Está diseñado para ejecutar aplicaciones web que siguen los estándares **ASGI, RSGI y WSGI**.

# Ejecución de una aplicación web
granian --port 5000 --host 0.0.0.0 --http auto --workers 4 --blocking-threads 4 --backlog 2048 --interface wsgi wsgi:app

# Documentación
https://github.com/emmett-framework/granian


# Requisitos generales

1. Tener Docker Desktop instalado.
2. Configurar archivo .env.



# 1. Requisitos previos de infraestructura

Antes de levantar el microservicio de alumnos necesitás:

- **Docker Desktop** instalado y funcionando.
- Proyecto de infraestructura del profesor levantado, que incluye:
  - `postgresql-servidor` (PostgreSQL)
  - `redis` (Redis)
  - `pgadmin` (pgAdmin4)
  - `traefik` (reverse proxy)
- Red Docker externa creada (si no existe).

## Crear la red
docker network create mired


# Certificados y Traefik

Traefik es un proxy inverso y balanceador de carga, nativo de la nube y de código abierto, que facilita la implementación de microservicios.

## Estructura de Traefik
carpeta_del_usuario
├── traefik
│   ├── certs 
│   ├── config      # Carpeta de configuración de Traefik
│   └── docker-compose.yml


# Utilidad para generar certificados (mkcert)

Para generar e instalar certificados para desarrollo se puede utilizar **mkcert**.

1. Descargar mkcert: https://github.com/FiloSottile/mkcert/tags

2. Agregar en C:\Windows\System32\drivers\etc\hosts
 al final del archivo:
   127.0.0.1 traefik.universidad.localhost
   127.0.0.1 alumno-backend.universidad.localhost
   127.0.0.1 whoami.universidad.localhost
3. Generar certificados:
   mkcert -cert-file certs/cert.pem -key-file certs/key.pem "universidad.localhost" "*.universidad.localhost" 127.0.0.1 ::1

4. Instalar certificados:
   mkcert -install

Los archivos key.pem y cert.pem deben copiarse en la carpeta **certs** de Traefik.

## Documentación
- mkcert: https://github.com/FiloSottile/mkcert
- Traefik: https://doc.traefik.io/traefik/


# Crear .env para Traefik

Estructura de carpetas (infra del profesor, ejemplo):
MSALUMNOS/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── resources/
│   └── services/
├── traefik/
│   ├── docker-compose.yml
│   └── .env   <- LO CREAMOS NOSOTROS
└── wsgi.py

El .env se crea según un archivo de ejemplo (env-example) provisto.  
Una vez creado el .env, ubicarse en la carpeta donde está el docker-compose de Traefik y ejecutar:
docker compose up

URLs para acceder:
- PgAdmin: https://pgadmin.universidad.localhost/login?next=/
- Traefik Dashboard: https://traefik.universidad.localhost/dashboard/#/


# Crear servidor en PgAdmin

Dentro de PgAdmin:
1. Crear un nuevo servidor.
2. Configurarlo según los parámetros que se definieron en el .env de Traefik (host, puerto, usuario, contraseña, base de datos).
3. Es importante que todo concuerde y siempre se usen las mismas variables de entorno.



# Cargar alumnos (opcional, solo para probar el microservicio)

Dentro de la base de datos asociada al servidor (por ejemplo `test_sysacad`):

1. Una vez creada la base de datos, hacer clic derecho en la base y seleccionar:  
   Query Tool (Alt + Shift + Q).

2. Ejecutar el siguiente script SQL:
-- Borrar tablas existentes

DROP TABLE IF EXISTS alumnos CASCADE;
DROP TABLE IF EXISTS tipo_documento CASCADE;

-- Tabla tipo_documento
CREATE TABLE tipo_documento (
    id      SERIAL PRIMARY KEY,
    sigla   VARCHAR(10) NOT NULL,
    nombre  VARCHAR(100) NOT NULL
);

-- Tabla alumnos
CREATE TABLE alumnos (
    id               INTEGER PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    apellido         VARCHAR(100) NOT NULL,
    nro_documento    INTEGER NOT NULL,
    tipo_documento   VARCHAR(10) NOT NULL,
    sexo             VARCHAR(1) NOT NULL,
    nro_legajo       INTEGER NOT NULL,
    especialidad_id  INTEGER NOT NULL
);

-- Datos base para tipo_documento
INSERT INTO tipo_documento (sigla, nombre) VALUES
('DNI', 'Documento Nacional de Identidad'),
('LE',  'Libreta de Enrolamiento'),
('LC',  'Libreta Cívica'),
('PAS', 'Pasaporte');

-- Ejemplos de alumnos (adaptados a tu nuevo modelo)
INSERT INTO alumnos (
    id, nombre, apellido, nro_documento, tipo_documento,
    sexo, nro_legajo, especialidad_id
)
VALUES
    (1, 'Juan',  'Pérez',     40123456, 'DNI', 'M', 1001, 10),
    (2, 'Ana',   'Gómez',     39222111, 'DNI', 'F', 1002, 11),
    (3, 'Lucas', 'Rodríguez', 1234567,  'PAS', 'M', 1003, 12),
    (4, 'Sofía', 'López',     30555111, 'DNI', 'F', 1004, 13);


# Crear .env para el microservicio MSALUMNOS (Docker)

Estructura de ejemplo:
MSALUMNOS/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── resources/
│   └── services/
├── docker/
│   ├── docker-compose.yml
│   └── .env   <- LO CREAMOS NOSOTROS
└── wsgi.py

El .env se crea según el env-example del microservicio

# Crear imagen
ubicarse en la raiz del proyecto
docker build -t gestion-alumnos:v1.0.0 .

# Levantar el microservicio de alumnos

Ubicarse en la carpeta `docker` del proyecto MSALUMNOS (donde está el `docker-compose.yml`).

Si es la primera vez:
docker compose up --build

Si ya se construyó la imagen previamente:
docker compose up


# Endpoints del microservicio

Alumnos – GET (todos):
http://alumnos.universidad.localhost/api/v1/alumno

Alumnos – GET por ID:
http://alumnos.universidad.localhost/api/v1/alumno/1

