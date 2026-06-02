from __future__ import annotations

import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=32, unique=True)
    email = models.EmailField(blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(null=True, blank=True)

    visits_count = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    manual_discount_percent = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Если задано — перекрывает авто-скидку")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone"]),
        ]

    def __str__(self) -> str:
        return self.full_name or self.phone

    @property
    def auto_discount_percent(self) -> int:
        spent = self.total_spent or 0
        # Правила накопительной скидки по сумме всех заказов:
        # До 5 000 ₽ = 0%
        # 5 000 - 15 000 ₽ = 3%
        # 15 000 - 30 000 ₽ = 5%
        # 30 000 - 60 000 ₽ = 7%
        # 60 000 - 100 000 ₽ = 10%
        # Больше 100 000 ₽ = 12%
        if spent >= 100_000:
            return 12
        if spent >= 60_000:
            return 10
        if spent >= 30_000:
            return 7
        if spent >= 15_000:
            return 5
        if spent >= 5_000:
            return 3
        return 0

    @property
    def discount_percent(self) -> int:
        return int(self.manual_discount_percent) if self.manual_discount_percent is not None else self.auto_discount_percent

    @property
    def birthday_discount_percent(self) -> int:
        if not self.birthday:
            return 0
        today = timezone.localdate()
        if self.birthday.month == today.month and self.birthday.day == today.day:
            return 50
        return 0


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts_left = models.PositiveSmallIntegerField(default=5)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["phone", "created_at"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self) -> str:
        return f"OTP {self.phone} ({self.created_at:%Y-%m-%d %H:%M})"

    @classmethod
    def issue(cls, phone: str, ttl_minutes: int = 5) -> "PhoneOTP":
        code = f"{secrets.randbelow(10**6):06d}"
        now = timezone.now()
        return cls.objects.create(
            phone=phone,
            code=code,
            expires_at=now + timedelta(minutes=ttl_minutes),
        )

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at


class OperationLog(models.Model):
    class Kind(models.TextChoices):
        VISIT_COUNTED = "visit_counted", "Засчитан визит"
        EVENT_REGISTERED = "event_registered", "Запись на мероприятие"
        EVENT_CANCELLED = "event_cancelled", "Отмена записи"
        REVIEW_CREATED = "review_created", "Отправлен отзыв"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="operations")
    kind = models.CharField(max_length=32, choices=Kind.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    percent = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "created_at"])]

