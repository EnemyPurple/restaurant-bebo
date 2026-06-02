from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from datetime import timedelta

from django.utils import timezone

from .models import Event, EventRegistration
from apps.users.models import OperationLog


def events_list(request):
    events = Event.objects.filter(is_published=True).order_by("date_start")
    return render(request, "events/list.html", {"events": events})


def event_detail(request, slug: str):
    event = get_object_or_404(Event, is_published=True, slug=slug)
    registration = None
    if request.user.is_authenticated:
        registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    return render(request, "events/detail.html", {"event": event, "registration": registration})


@login_required
def register_for_event(request, slug: str):
    event = get_object_or_404(Event, is_published=True, slug=slug)
    reg, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
    if not created and reg.is_cancelled:
        reg.is_cancelled = False
        reg.cancelled_at = None
        reg.save(update_fields=["is_cancelled", "cancelled_at"])
    OperationLog.objects.create(user=request.user, kind=OperationLog.Kind.EVENT_REGISTERED, description=f"Запись на «{event.title}»")
    messages.success(request, "Вы записались на мероприятие.")
    return redirect(event.get_absolute_url())


@login_required
def cancel_registration(request, slug: str):
    event = get_object_or_404(Event, is_published=True, slug=slug)
    reg = EventRegistration.objects.filter(user=request.user, event=event, is_cancelled=False).first()
    if not reg:
        messages.info(request, "Запись не найдена.")
        return redirect(event.get_absolute_url())

    if event.date_start - timezone.now() < timedelta(hours=24):
        messages.error(request, "Отменить запись можно не позднее чем за 24 часа до начала.")
        return redirect(event.get_absolute_url())

    reg.is_cancelled = True
    reg.cancelled_at = timezone.now()
    reg.save(update_fields=["is_cancelled", "cancelled_at"])
    OperationLog.objects.create(user=request.user, kind=OperationLog.Kind.EVENT_CANCELLED, description=f"Отмена записи на «{event.title}»")
    messages.success(request, "Запись отменена.")
    return redirect(event.get_absolute_url())

