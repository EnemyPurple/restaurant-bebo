from __future__ import annotations

import time
from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse


class DevTunnelCookieMiddleware:
    """Secure cookies over HTTPS tunnel; plain cookies on local http://127.0.0.1."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.META.get("HTTP_X_FORWARDED_PROTO") == "https":
            settings.SESSION_COOKIE_SECURE = True
            settings.CSRF_COOKIE_SECURE = True
        else:
            settings.SESSION_COOKIE_SECURE = False
            settings.CSRF_COOKIE_SECURE = False
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """
    Минимальный набор заголовков безопасности + базовая CSP.
    CSP здесь намеренно «мягкая», чтобы не ломать Bootstrap/CDN; при деплое её обычно ужесточают.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https:; "
            "script-src 'self' 'unsafe-inline' https:; font-src 'self' data: https:; connect-src 'self' https:; "
            "frame-src 'self' https://yandex.ru https://*.yandex.ru https://*.yandex.net "
            "https://www.google.com https://maps.google.com https://*.google.com;",
        )
        if not settings.DEBUG:
            response.headers.setdefault("Strict-Transport-Security", "max-age=2592000; includeSubDomains; preload")
        return response


@dataclass(frozen=True)
class RateLimitRule:
    key_prefix: str
    rate: int
    per_seconds: int


class RateLimitMiddleware:
    """
    Простой rate limiting на основе Django cache (Redis в docker-compose).
    Лимитируем только чувствительные POST формы.
    """

    RULES: dict[str, RateLimitRule] = {
        "/booking/": RateLimitRule("rl:booking", rate=20, per_seconds=60),
        "/contacts/": RateLimitRule("rl:contacts", rate=20, per_seconds=60),
        "/newsletter/subscribe/": RateLimitRule("rl:newsletter", rate=30, per_seconds=60),
        "/admin/login/": RateLimitRule("rl:admin_login", rate=10, per_seconds=60),
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST":
            for path_prefix, rule in self.RULES.items():
                if request.path.startswith(path_prefix):
                    if self._is_limited(request, rule):
                        return HttpResponse("Too Many Requests", status=429)
                    break
        return self.get_response(request)

    def _is_limited(self, request: HttpRequest, rule: RateLimitRule) -> bool:
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")
        if not ip:
            return False
        window = int(time.time()) // rule.per_seconds
        key = f"{rule.key_prefix}:{ip}:{window}"
        current = cache.get(key, 0)
        if current >= rule.rate:
            return True
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=rule.per_seconds + 5)
        return False

