import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PROD")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "app/generated_cvs")
    TOKEN_TTL = 600  # 10 minutes

    RATELIMIT_DEFAULT = "200 per day;50 per hour"
