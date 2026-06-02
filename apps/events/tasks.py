from __future__ import annotations

from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import EventRegistration


@shared_task
def send_event_reminders_task() -> int:
    """
    Напоминание за ~1 день до события.
    В проде обычно запускается через celery beat (периодически).
    """
    now = timezone.now()
    start = now + timedelta(hours=23)
    end = now + timedelta(hours=25)

    regs = (
        EventRegistration.objects.filter(is_cancelled=False, event__date_start__gte=start, event__date_start__lte=end)
        .select_related("event", "user")[:500]
    )
    sent = 0
    for r in regs:
        email = getattr(getattr(r.user, "profile", None), "email", "") or getattr(r.user, "email", "")
        if not email:
            continue
        subject = f"Бебо: напоминание о событии «{r.event.title}»"
        body = (
            f"Здравствуйте!\n\n"
            f"Напоминаем о мероприятии:\n"
            f"{r.event.title}\n"
            f"Начало: {timezone.localtime(r.event.date_start):%d.%m.%Y %H:%M}\n\n"
            f"Адрес и детали уточняйте на сайте.\n"
        )
        send_mail(subject, body, None, [email], fail_silently=True)
        sent += 1
    return sent

