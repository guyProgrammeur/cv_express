from flask import Flask
from .config import Config
from .extensions import cors, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors.init_app(app)
    limiter.init_app(app)

    from .api.cv_routes import cv_bp
    from .api.download_routes import download_bp

    app.register_blueprint(cv_bp, url_prefix='/api/v1')
    app.register_blueprint(download_bp)

    return app
