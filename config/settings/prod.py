from .base import *  # noqa: F403
import os

DEBUG = False

BUNDLED_MEDIA_MODE = "full"  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
_render_url = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")

if _render_host:
    ALLOWED_HOSTS = list({*ALLOWED_HOSTS, _render_host, ".onrender.com"})  # noqa: F405

_csrf_origins = set(CSRF_TRUSTED_ORIGINS)  # noqa: F405
if _render_host:
    _csrf_origins.add(f"https://{_render_host}")
if _render_url:
    _csrf_origins.add(_render_url)
CSRF_TRUSTED_ORIGINS = sorted(_csrf_origins)  # noqa: F405

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # type: ignore[name-defined] # noqa: F405
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)  # type: ignore[name-defined] # noqa: F405
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)  # type: ignore[name-defined] # noqa: F405

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

