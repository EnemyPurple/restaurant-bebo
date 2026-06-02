from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import ContactMessage, ContactSettings


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at", "ip_address")
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("created_at", "ip_address")


@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Контактная информация", {"fields": ("address", "phone", "working_hours")}),
        (
            "Карта",
            {
                "fields": ("map_embed_url", "map_longitude", "map_latitude", "map_zoom"),
                "description": (
                    "Чтобы сменить карту: откройте Яндекс.Карты, найдите место → Поделиться → "
                    "«Код для сайта» → скопируйте значение src из iframe и вставьте в поле выше. "
                    "Либо укажите координаты и масштаб — карта построится автоматически."
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not ContactSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        settings_obj = ContactSettings.load()
        return redirect(reverse("admin:contacts_contactsettings_change", args=(settings_obj.pk,)))

