from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from slugify import slugify


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="events/", blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    max_guests = models.PositiveIntegerField(default=0, help_text="0 = без ограничения")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date_start"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published", "date_start"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("events:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "event"], name="uniq_event_registration_user_event"),
        ]
        indexes = [
            models.Index(fields=["event", "is_cancelled"]),
            models.Index(fields=["user", "is_cancelled"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.event}"
