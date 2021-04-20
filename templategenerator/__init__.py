import os

from flask import Flask


project_dir = os.path.dirname(os.path.abspath(__file__))


def create_app():
    """Creates flask app and pushes context.

    Returns:
        app: the Flask application object
    """
    app = Flask(__name__)
    app.app_context().push()

    return app
