from .base import *  # noqa: F403

DEBUG = True

# Локально админка — источник правды; manifest не перезаписывает БД.
BUNDLED_MEDIA_MODE = "preserve"  # noqa: F405

# Для туннеля (localhost.run / cloudflare): разрешить любой Host в dev.
if "*" in ALLOWED_HOSTS:  # noqa: F405
    ALLOWED_HOSTS = ["*"]  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MIDDLEWARE = [  # noqa: F405
    "apps.core.middleware.DevTunnelCookieMiddleware",
    *MIDDLEWARE,
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Удобно для разработки/тестов: не требовать поднятый Redis для Celery.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_RESULT_BACKEND = "cache+memory://"

# В dev режиме не требуем Redis для кэша (иначе падают страницы, которые читают cache).
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "bebo-dev",
    }
}

