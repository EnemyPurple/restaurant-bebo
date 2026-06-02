from __future__ import annotations

import logging

from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking
from .tasks import send_booking_email_task
from apps.users.models import OperationLog, Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Booking)
def booking_created(sender, instance: Booking, created: bool, **kwargs):
    if created:
        def enqueue_booking_email() -> None:
            try:
                send_booking_email_task.delay(instance.id)
            except Exception:
                # Бронирование не должно падать, даже если брокер задач недоступен.
                logger.exception("Failed to enqueue booking email task for booking_id=%s", instance.id)

        transaction.on_commit(enqueue_booking_email)

    # Накопительная система: засчитываем визит при первом подтверждении.
    if instance.user_id and instance.status == Booking.Status.CONFIRMED and not instance.is_visit_counted:
        Profile.objects.filter(user_id=instance.user_id).update(
            visits_count=F("visits_count") + 1,
            total_spent=F("total_spent") + instance.spent_amount,
        )
        Booking.objects.filter(id=instance.id).update(is_visit_counted=True)
        OperationLog.objects.create(
            user_id=instance.user_id,
            kind=OperationLog.Kind.VISIT_COUNTED,
            amount=instance.spent_amount,
            description=f"Визит по брони #{instance.id} ({instance.date} {instance.time})",
        )

