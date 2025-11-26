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


