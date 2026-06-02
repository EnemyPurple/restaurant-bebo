from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import ContactSettings


def contacts_page(request):
    contact_settings = ContactSettings.load()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = request.META.get("REMOTE_ADDR")
            msg.save()
            messages.success(request, "Спасибо! Сообщение отправлено.")
            return redirect("contacts:contacts")
    else:
        form = ContactForm()
    return render(
        request,
        "contacts/contacts.html",
        {"form": form, "contact_settings": contact_settings},
    )
