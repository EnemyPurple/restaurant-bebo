from __future__ import annotations

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import BookingForm
from .models import Booking


def booking_page(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    booking: Booking = form.save(commit=False)
                    if request.user.is_authenticated:
                        booking.user = request.user
                    booking.save()
            except IntegrityError:
                form.add_error(None, "Этот столик уже забронирован на выбранное время. Выберите другое время/столик.")
            else:
                messages.success(request, "Заявка на бронирование отправлена. Мы свяжемся с вами для подтверждения.")
                return redirect("booking:success")
    else:
        form = BookingForm()
    return render(request, "booking/booking.html", {"form": form})


def booking_success(request):
    return render(request, "booking/success.html")

