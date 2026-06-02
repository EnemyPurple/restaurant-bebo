from .base import *  # noqa: F403
import os

DEBUG = False

_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if _render_host:
    ALLOWED_HOSTS = list({*ALLOWED_HOSTS, _render_host, ".onrender.com"})  # noqa: F405
    CSRF_TRUSTED_ORIGINS = list(  # noqa: F405
        {*CSRF_TRUSTED_ORIGINS, f"https://{_render_host}", "https://*.onrender.com"}
    )

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # type: ignore[name-defined] # noqa: F405
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)  # type: ignore[name-defined] # noqa: F405
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)  # type: ignore[name-defined] # noqa: F405

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

