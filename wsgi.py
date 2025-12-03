from app import create_app
import logging

app = create_app()
app.app_context().push()
