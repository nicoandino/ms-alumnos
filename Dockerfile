# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY pyproject.toml .

# Instalar uv
RUN pip install uv

# Instalar dependencias
RUN uv sync --no-dev

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando de ejecución
CMD ["python", "app.py"]
