from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer

cors = CORS()
limiter = Limiter(get_remote_address)

serializer = None

def init_serializer(app):
    global serializer
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
