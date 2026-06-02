from __future__ import annotations

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Profile


@shared_task
def send_birthday_congrats_task() -> int:
    today = timezone.localdate()
    profiles = Profile.objects.filter(birthday__month=today.month, birthday__day=today.day)[:1000]
    sent = 0
    for p in profiles:
        if not p.email:
            continue
        subject = "Бебо: поздравляем с днём рождения!"
        body = (
            f"Здравствуйте, {p.full_name or p.phone}!\n\n"
            f"Поздравляем с днём рождения!\n"
            f"Сегодня для вас действует скидка 50%.\n"
        )
        send_mail(subject, body, None, [p.email], fail_silently=True)
        sent += 1
    return sent

