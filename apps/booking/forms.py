from __future__ import annotations

import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from apps.core.forms import BootstrapFormMixin

from .models import Booking, Table

PHONE_RE = re.compile(r"^\+?\d[\d\-\s\(\)]{7,}$")


class BookingForm(BootstrapFormMixin, forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, required=False)

    class Meta:
        model = Booking
        fields = ["name", "phone", "email", "date", "time", "guests", "table", "comment"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["table"].queryset = Table.objects.filter(is_active=True).order_by("number")
        if not (getattr(settings, "RECAPTCHA_PUBLIC_KEY", "") and getattr(settings, "RECAPTCHA_PRIVATE_KEY", "")):
            self.fields.pop("captcha", None)

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not PHONE_RE.match(phone):
            raise ValidationError("Введите корректный номер телефона.")
        return phone

