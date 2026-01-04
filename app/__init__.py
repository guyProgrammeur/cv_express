from flask import Flask
from .config import DevConfig, ProdConfig
from .extensions import cors, limiter, init_serializer
import os
from dotenv import load_dotenv

# Charger l'env au tout début
load_dotenv()

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)


    # Vérifie que SECRET_KEY est bien lu
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is not configured. Vérifie ton .env ou config.py")

    cors.init_app(app, resources=app.config.get("CORS_RESOURCES", {}))
    limiter.init_app(app)
    init_serializer(app)

    from .api.cv_routes import cv_bp
    app.register_blueprint(cv_bp, url_prefix="/api")

    from .api.download_routes import download_bp 
    app.register_blueprint(download_bp, url_prefix="/api")

    return app
