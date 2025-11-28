FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# El usuario de la app
RUN useradd --create-home --home-dir /home/flaskapp flaskapp

RUN apt-get update && \
    apt-get install -y python3-dev build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp
USER flaskapp

# Instalar UV
RUN curl -fsSL https://astral.sh/uv/install.sh -o uv-installer.sh \
    && sh uv-installer.sh \
    && rm uv-installer.sh

ENV PATH="/home/flaskapp/.local/bin:${PATH}"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked

COPY app ./app
COPY wsgi.py .

EXPOSE 5000

CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--interface", "wsgi", "wsgi:app"]
