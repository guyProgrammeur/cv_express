from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from itsdangerous import URLSafeTimedSerializer
import os

# -------------------
# CORS
# -------------------
cors = CORS()

# -------------------
# Client IP resolution (Cloudflare + Reverse proxy safe)
# -------------------
def get_client_ip():
    """
    Résout l'IP réelle du client derrière Cloudflare / Apache.
    L'ordre est volontairement strict pour éviter le spoofing.
    """
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip

    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()

    return request.remote_addr


# -------------------
# Rate limiter (Redis-backed)
# -------------------
limiter = Limiter(
    key_func=get_client_ip,
    storage_uri=os.getenv("REDIS_URL", "redis://127.0.0.1:6379"),
    default_limits=[
        "200 per day",
        "50 per hour"
    ],
    strategy="fixed-window"
)

# -------------------
# Token serializer (downloads sécurisés)
# -------------------
serializer: URLSafeTimedSerializer | None = None


def init_serializer(app):
    global serializer

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is not configured")

    serializer = URLSafeTimedSerializer(
        secret_key=app.config["SECRET_KEY"],
        salt="cv-download-token"
    )
