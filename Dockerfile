FROM python:3.14-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.venv/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp
RUN apt-get update
RUN apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

USER flaskapp

ADD https://astral.sh/uv/install.sh ./uv-installer.sh
RUN sh ./uv-installer.sh && rm ./uv-installer.sh

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

COPY ./app ./app
COPY ./wsgi.py .

RUN chown -R flaskapp:flaskapp /home/flaskapp


ENV VIRTUAL_ENV="/home/flaskapp/.venv"

EXPOSE 5000
CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]
