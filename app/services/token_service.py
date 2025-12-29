from itsdangerous import SignatureExpired
from flask import current_app
from ..extensions import serializer

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def get_serializer():
    secret_key = current_app.config.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY manquante pour la génération des tokens")

    return URLSafeTimedSerializer(secret_key, salt="cv-download")

def generate_token(filename: str, transaction_id: str) -> str:
    serializer = get_serializer()
    return serializer.dumps({
        "filename": filename,
        "transaction_id": transaction_id
    })

def verify_token(token: str, max_age: int = 600):
    serializer = get_serializer()
    return serializer.loads(token, max_age=max_age)
