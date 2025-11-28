FROM python:3.11-slim

# Instalamos dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalamos uv
RUN curl -fsSL https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copiar solo el pyproject primero (mejor cache)
COPY pyproject.toml .

# Crear entorno virtual e instalar dependencias
RUN uv sync --no-dev

# Copiar el resto del proyecto
COPY . .

# Exponer puerto
EXPOSE 5000

# Asegurar que ejecutamos dentro del .venv
CMD [".venv/bin/python", "app.py"]
