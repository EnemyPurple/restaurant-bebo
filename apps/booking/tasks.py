from __future__ import annotations

from celery import shared_task
from django.core.mail import send_mail

from .models import Booking


@shared_task
def send_booking_email_task(booking_id: int) -> None:
    booking = Booking.objects.select_related("table").get(id=booking_id)
    if not booking.email:
        return
    subject = "Бебо: заявка на бронирование получена"
    body = (
        f"Здравствуйте, {booking.name}!\n\n"
        f"Мы получили вашу заявку на бронирование.\n"
        f"Дата: {booking.date}\n"
        f"Время: {booking.time}\n"
        f"Гостей: {booking.guests}\n"
        f"Столик: #{booking.table.number}\n\n"
        f"Статус: {booking.get_status_display()}\n"
    )
    send_mail(subject, body, None, [booking.email], fail_silently=True)

