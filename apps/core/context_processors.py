from __future__ import annotations

from django.conf import settings

from apps.contacts.models import ContactSettings


def site_settings(request):
    return {
        "SITE_NAME": "Бебо",
        "DEBUG": settings.DEBUG,
        "contact_settings": ContactSettings.load(),
    }

