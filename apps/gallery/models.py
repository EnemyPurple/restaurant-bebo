from __future__ import annotations

from django.db import models


class GalleryImage(models.Model):
    class Category(models.TextChoices):
        INTERIOR = "interior", "Интерьер"
        FOOD = "food", "Еда"
        EVENT = "event", "События"

    title = models.CharField(max_length=160, blank=True)
    image = models.ImageField(upload_to="gallery/")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.INTERIOR)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_published", "category"]),
        ]

    def __str__(self) -> str:
        return self.title or f"Фото #{self.pk}"

