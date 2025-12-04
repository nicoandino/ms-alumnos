FROM python:3.14-slim

# Config básica de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias del sistema (para compilar paquetes como psycopg2)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Usuario para la app
RUN useradd --create-home --home-dir /home/flaskapp flaskapp

WORKDIR /home/flaskapp

# Instalamos uv dentro de la imagen
RUN pip install --no-cache-dir uv

# Copiamos solo archivos de dependencias para aprovechar cache
COPY pyproject.toml uv.lock ./

# Creamos el entorno virtual .venv y resolvemos dependencias con uv
# (por defecto uv crea /home/flaskapp/.venv al correr en este directorio)
RUN uv sync --frozen --no-dev

# Ahora copiamos el código de la aplicación
COPY app ./app
COPY wsgi.py .

# Permisos y usuario final
RUN chown -R flaskapp:flaskapp /home/flaskapp
USER flaskapp

# Activamos el venv en tiempo de ejecución
ENV VIRTUAL_ENV="/home/flaskapp/.venv"
ENV PATH="/home/flaskapp/.venv/bin:$PATH"

EXPOSE 5000

CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]
