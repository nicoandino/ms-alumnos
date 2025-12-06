
-- Borrar tablas si existen (respetando dependencias)
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
    id               SERIAL PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    apellido         VARCHAR(100) NOT NULL,
    nro_documento    INTEGER NOT NULL,
    tipo_documento_id INTEGER NOT NULL,
    sexo             VARCHAR(1) NOT NULL,
    nro_legajo       INTEGER NOT NULL,
    especialidad_id  INTEGER NOT NULL,
    CONSTRAINT fk_alumnos_tipo_documento
        FOREIGN KEY (tipo_documento_id)
        REFERENCES tipo_documento(id)
);

-- Datos base para tipo_documento
INSERT INTO tipo_documento (sigla, nombre) VALUES
('DNI', 'Documento Nacional de Identidad'),
('LE',  'Libreta de Enrolamiento'),
('LC',  'Libreta Cívica'),
('PAS', 'Pasaporte');

-- Ejemplos de alumnos usando tipo_documento_id
-- (no ponemos el id, deja que SERIAL lo genere solo)
INSERT INTO alumnos (
    nombre, apellido, nro_documento, tipo_documento_id,
    sexo, nro_legajo, especialidad_id
)
VALUES
    (
        'Juan',  'Pérez', 40123456,
        (SELECT id FROM tipo_documento WHERE sigla = 'DNI'),
        'M', 1001, 10
    ),
    (
        'Ana',   'Gómez', 39222111,
        (SELECT id FROM tipo_documento WHERE sigla = 'DNI'),
        'F', 1002, 11
    ),
    (
        'Lucas', 'Rodríguez', 1234567,
        (SELECT id FROM tipo_documento WHERE sigla = 'PAS'),
        'M', 1003, 12
    ),
    (
        'Sofía', 'López', 30555111,
        (SELECT id FROM tipo_documento WHERE sigla = 'DNI'),
        'F', 1004, 13
    );

