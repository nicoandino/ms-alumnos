# uv
## Instalación
1. Abrir **consola de PowerShell como administrador**.  
2. Instalar `uv`:
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
3. Reiniciar la PC.
## Crear Proyecto
```
uv init nombre-proyecto
uv init # si el proyecto ya existe
```
en nuestro caso ya existe, pq estarian copiando la carpeta del git

## Instalación de Envtorno Virtual venv
```
uv venv
```

## Agregar dependencias 
```
uv add flask==3.1.2 
```
## Sincronizar dependencias 
```
uv sync 
```
## Documentación
[Referencia: https://docs.astral.sh/uv/getting-started/first-steps/]

# Granian
Servidor HTTP de **alto rendimiento escrito** en **Rust** para **aplicaciones Python**. Está diseñado para ejecutar aplicaciones web que siguen los estándares **ASGI, RSGI y WSG**

## Ejecución de una Aplicación Web
```
granian --port 5000 --host 0.0.0.0 --http auto --workers 4 --blocking-threads 4 --backlog 2048 --interface wsgi wsgi:app
```
## Documentación
https://github.com/emmett-framework/granian


## requsitos
1. tener docker desktop
2. configurar .env
3. iniciar docker swarm en la terminal raiz del proyecto
docker swarm init



# configurar env
coomo docker swarm no lee .env , hay que hacerlo manualmente
en /docker/docker-compose.yml, dentro de ese archivo solamente tienen que modificar esta parte
    environment:
      FLASK_CONTEXT: production
      SQLALCHEMY_DATABASE_URI: postgresql+psycopg2://postgres:contraseña@host.docker.internal:5432/test_sysacad **
      HOST_DB: host.docker.internal
      USER_DB: postgres
      PASSWORD_DB: contraseña **
      NAME_DB: test_sysacad ** 
      REDIS_HOST: host.docker.internal
      REDIS_PORT: "6379"
      REDIS_PASSWORD: ""
tienen que modificar por lo que tengan ustedes, los que estan marcados con astericos son los que tendrian que modificar segun lo q tengan
NAME_DB: test_sysacad **  depende modificarla segun ustedes, yo use esa para probar

## cargar alumnos
tienen que modificar la linea 11 , colocando su URL con su base de datos, una vez hehcho
tienen que borrar cualquier tabla que exista en la base de datos para evitar errores
una vez que tengan la base de datos limpia, tienen que correr el archivo
alumnos_crear.py
verifiquen que les cargue los alumnos viendolo desde pgadmin o usando shell de postgres

## crear imagenes de docker
Esta imagen se crea en la raiz del proyecto
1. docker build -t gestion-alumnos:v1.0.0 
esa es la imagen del ms

2. docker pull traefik:v2.11
imagen de traefik

## crear red
docker network create --driver overlay mired

solo se crea una vez y listo

## antes de abrir el ms
tienen que tener el docker desktop abierto si o si 

les recomiendo abrir 3 terminales
1. cd docker 
2. cd traefik
3. para eliminar los contenedores

el uso de distintas terminales , es para que una este en la raiz de docker y la otra en la raiz de traefik, la tercera es opcional , pero es para no mezclar comandos
## iniciar ms
en la carpeta donde esta el docker-compose
usar en terminal 
--
cd docker
--
docker stack deploy -c docker-compose.yml 
--
se inicia el ms
## iniciar traefik
usar en terminal
--
cd traefik
--
docker stack deploy -c docker-traefik.yml traefik
--
se inicia docker

## verificar que funcionan
para ver que funcionen , los contenedores deben estar en funcionamiento en la pestaña de traefik
sino ejecutar en cualquier terminal
docker service ls

deberia aparecer
msalumnos_alumnos-service   3/3   Running
traefik_traefik             1/1   Running

## probar endpoints
Alumnos – GET
http://alumnos.universidad.localhost/api/v1/alumno

Alumnos – GET por ID
http://alumnos.universidad.localhost/api/v1/alumno/1

## ver traefik
http://traefik.universidad.localhost:8080


## detener los contenedores
estos comandos se pueden poner en cualquier terminal 
docker stack rm traefik
docker stack rm msalumnos
