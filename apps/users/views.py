from __future__ import annotations

from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.booking.models import Booking
from apps.events.models import EventRegistration
from apps.users.models import OperationLog

from .forms import PhoneLoginRequestForm, PhoneLoginVerifyForm, ProfileRegistrationForm
from .models import PhoneOTP, Profile

User = get_user_model()


def phone_login_request(request):
    if request.user.is_authenticated:
        return redirect("users:cabinet")
    if request.method == "POST":
        form = PhoneLoginRequestForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = PhoneOTP.issue(phone=phone)
            # Имитация SMS: в dev показываем код в сообщении (в проде отправляйте через SMS API).
            messages.info(request, f"Код подтверждения (DEV): {otp.code}")
            next_url = (request.GET.get("next") or request.POST.get("next") or "").strip()
            qs = {"phone": phone}
            if next_url:
                qs["next"] = next_url
            return redirect(f"{reverse('users:login_verify')}?{urlencode(qs)}")
    else:
        form = PhoneLoginRequestForm()
    return render(request, "users/login.html", {"form": form, "next": (request.GET.get("next") or "").strip()})


def phone_login_verify(request):
    if request.user.is_authenticated:
        return redirect("users:cabinet")
    phone = (request.GET.get("phone") or request.POST.get("phone") or "").strip()
    next_url = (request.GET.get("next") or request.POST.get("next") or "").strip()
    if request.method == "POST":
        form = PhoneLoginVerifyForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"].strip()
            code = form.cleaned_data["code"].strip()
            otp = (
                PhoneOTP.objects.filter(phone=phone, is_used=False, expires_at__gt=timezone.now())
                .order_by("-created_at")
                .first()
            )
            if not otp:
                form.add_error(None, "Код истёк. Запросите новый.")
            else:
                if otp.attempts_left <= 0:
                    form.add_error(None, "Слишком много попыток. Запросите новый код.")
                elif otp.code != code:
                    otp.attempts_left -= 1
                    otp.save(update_fields=["attempts_left"])
                    form.add_error("code", "Неверный код.")
                else:
                    otp.is_used = True
                    otp.save(update_fields=["is_used"])

                    user, created = User.objects.get_or_create(username=phone)
                    profile, _ = Profile.objects.get_or_create(user=user, defaults={"phone": phone})
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                    # Если профиль ещё не заполнен — предложим регистрацию.
                    if not (profile.full_name or profile.email or profile.birthday):
                        return redirect("users:register")
                    return redirect(next_url or "users:cabinet")
    else:
        form = PhoneLoginVerifyForm(initial={"phone": phone})
    return render(request, "users/verify.html", {"form": form, "next": next_url})


@login_required
def register_profile(request):
    profile = getattr(request.user, "profile", None)
    if not profile:
        profile = Profile.objects.create(user=request.user, phone=request.user.username)

    if request.method == "POST":
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            profile.full_name = form.cleaned_data.get("full_name") or ""
            profile.email = form.cleaned_data.get("email") or ""
            profile.birthday = form.cleaned_data.get("birthday")
            profile.save(update_fields=["full_name", "email", "birthday"])
            messages.success(request, "Профиль сохранён.")
            return redirect("users:cabinet")
    else:
        form = ProfileRegistrationForm(
            initial={"full_name": profile.full_name, "email": profile.email, "birthday": profile.birthday}
        )
    return render(request, "users/register.html", {"form": form})


@login_required
def edit_profile(request):
    profile = getattr(request.user, "profile", None)
    if not profile:
        profile = Profile.objects.create(user=request.user, phone=request.user.username)

    if request.method == "POST":
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            profile.full_name = form.cleaned_data.get("full_name") or ""
            profile.email = form.cleaned_data.get("email") or ""
            profile.birthday = form.cleaned_data.get("birthday")
            profile.save(update_fields=["full_name", "email", "birthday"])
            messages.success(request, "Профиль обновлён.")
            return redirect("users:cabinet")
    else:
        form = ProfileRegistrationForm(
            initial={"full_name": profile.full_name, "email": profile.email, "birthday": profile.birthday}
        )
    return render(request, "users/edit_profile.html", {"form": form, "profile": profile})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def cabinet(request):
    profile = getattr(request.user, "profile", None)
    bookings = Booking.objects.filter(user=request.user).select_related("table").order_by("-created_at")[:50]
    registrations = (
        EventRegistration.objects.filter(user=request.user, is_cancelled=False)
        .select_related("event")
        .order_by("event__date_start")[:50]
    )
    operations = OperationLog.objects.filter(user=request.user).order_by("-created_at")[:50]
    return render(
        request,
        "users/cabinet.html",
        {
            "profile": profile,
            "bookings": bookings,
            "registrations": registrations,
            "operations": operations,
        },
    )

