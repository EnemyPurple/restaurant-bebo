from __future__ import annotations

from decimal import Decimal

from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}: {self.subject or 'Сообщение'}"


class ContactSettings(models.Model):
    """Единственная запись с контактами и картой — редактируется в админке."""

    address = models.CharField("Адрес", max_length=255, default="Йошкар-Ола, ул. Ленина, 1")
    phone = models.CharField("Телефон", max_length=64, default="8 800 555-35-35")
    working_hours = models.CharField("Часы работы", max_length=120, default="ежедневно 10:00–23:00")
    map_embed_url = models.URLField(
        "Ссылка для встраивания карты",
        max_length=500,
        blank=True,
        help_text=(
            "Скопируйте src из iframe: Яндекс.Карты → Поделиться → Код для сайта. "
            "Если оставить пустым, карта строится по координатам ниже."
        ),
    )
    map_longitude = models.DecimalField(
        "Долгота",
        max_digits=9,
        decimal_places=6,
        default=Decimal("47.894742"),
    )
    map_latitude = models.DecimalField(
        "Широта",
        max_digits=9,
        decimal_places=6,
        default=Decimal("56.634407"),
    )
    map_zoom = models.PositiveSmallIntegerField("Масштаб", default=16)

    class Meta:
        verbose_name = "Контакты и карта"
        verbose_name_plural = "Контакты и карта"

    def __str__(self) -> str:
        return "Контакты и карта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls) -> ContactSettings:
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_map_embed_url(self) -> str:
        if self.map_embed_url:
            return self.map_embed_url
        lon = self.map_longitude
        lat = self.map_latitude
        zoom = self.map_zoom
        return (
            f"https://yandex.ru/map-widget/v1/"
            f"?ll={lon}%2C{lat}&z={zoom}&pt={lon},{lat},pm2rdl"
        )

