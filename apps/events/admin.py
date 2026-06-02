from django.contrib import admin

from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date_start", "date_end", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "is_cancelled", "created_at", "cancelled_at")
    list_filter = ("is_cancelled", "event")
    search_fields = ("user__username", "event__title")
    readonly_fields = ("created_at",)

