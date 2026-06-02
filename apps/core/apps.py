from __future__ import annotations

from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


def sync_bundled_media_after_migrate(sender, **kwargs):
    if sender.name != "apps.core":
        return
    call_command("sync_bundled_media", verbosity=0)


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        post_migrate.connect(sync_bundled_media_after_migrate, dispatch_uid="sync_bundled_media")
