FROM python:3.14-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/flaskapp/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2 curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /root/app

COPY pyproject.toml uv.lock ./

RUN pip install .
RUN useradd --create-home --home-dir /home/flaskapp flaskapp

WORKDIR /home/flaskapp
COPY app ./app
COPY wsgi.py .

RUN chown -R flaskapp:flaskapp /home/flaskapp
USER flaskapp

EXPOSE 5000
CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]
