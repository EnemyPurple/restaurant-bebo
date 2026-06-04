from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.timezone import now

from .models import Subscriber


def newsletter_page(request):
    return render(request, "newsletter/subscribe.html")


def subscribe(request):
    if request.method != "POST":
        return redirect("home")
    email = (request.POST.get("email") or "").strip().lower()
    if not email or "@" not in email:
        messages.error(request, "Введите корректный email.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    sub, created = Subscriber.objects.get_or_create(email=email, defaults={"confirmed_at": now()})
    if not created:
        sub.is_active = True
        if not sub.confirmed_at:
            sub.confirmed_at = now()
        sub.save(update_fields=["is_active", "confirmed_at"])
    messages.success(request, "Вы подписались на новости.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

