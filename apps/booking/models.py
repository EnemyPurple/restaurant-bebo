from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Table(models.Model):
    class Location(models.TextChoices):
        HALL = "hall", "Зал"
        TERRACE = "terrace", "Терраса"
        VIP = "vip", "VIP"

    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=20, choices=Location.choices, default=Location.HALL)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return f"Столик #{self.number} ({self.seats} мест)"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        CONFIRMED = "confirmed", "Подтверждено"
        CANCELLED = "cancelled", "Отменено"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)

    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField(blank=True)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    spent_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Сумма чека (для накопительной скидки). Можно заполнить позже в админке.",
    )
    is_visit_counted = models.BooleanField(
        default=False,
        help_text="Отмечается автоматически при подтверждении, чтобы не засчитывать посещение дважды.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["date", "time", "table"]),
            models.Index(fields=["status", "date"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["table", "date", "time"], name="uniq_table_booking_slot"),
        ]

    def __str__(self) -> str:
        return f"Бронь {self.date} {self.time} — {self.name} (столик {self.table.number})"

