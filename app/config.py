import os
from dotenv import load_dotenv

# Charger .env dès le début
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set in production")

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
    DOWNLOAD_TOKEN_EXPIRATION = int(os.getenv("DOWNLOAD_TOKEN_EXPIRATION", 900))

    # Dossier de sortie pour les CV générés
    OUTPUT_DIR = os.path.join(BASE_DIR, "generated_cvs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # créer automatiquement si inexistant

    # Sécurité des cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True       # cookies uniquement via HTTPS
    SESSION_COOKIE_SAMESITE = "Lax"
    PREFERRED_URL_SCHEME = "https"

class DevConfig(BaseConfig):
    DEBUG = True
    CORS_RESOURCES = {r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}}

class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    # Autoriser uniquement ton domaine Cloudflare
    allowed_origins = os.getenv("CORS_ORIGINS")
    if not allowed_origins:
        raise RuntimeError("CORS_ORIGINS must be set in production")

    CORS_RESOURCES = {r"/api/*": {"origins": allowed_origins.split(",")}}

    # Rate limiting (si Flask-Limiter est utilisé)
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per hour")
    RATELIMIT_STORAGE_URL = BaseConfig.REDIS_URL
