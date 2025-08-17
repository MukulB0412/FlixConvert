from flask import Flask
from .routes import bp
import os

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300MB
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
    app.register_blueprint(bp)
    return app