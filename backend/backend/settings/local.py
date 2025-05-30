from os import getenv, path

from .base import *  # noqa
from .base import BASE_DIR

def get_secret(key, default):
    value = getenv(key, default)
    if path.isfile(value):
        with open(value) as f:
            return f.read()
    return value

SECRET_KEY = get_secret("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = get_secret("ADMIN_URL", "")

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024