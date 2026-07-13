from decouple import config

from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Serve static files efficiently in production via WhiteNoise if installed.
# Add "whitenoise.middleware.WhiteNoiseMiddleware" to MIDDLEWARE (right after
# SecurityMiddleware) and "whitenoise" to requirements.txt if you choose to
# deploy this way (e.g. on Render or Railway).
