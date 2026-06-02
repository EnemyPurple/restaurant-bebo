from __future__ import annotations

from django import forms
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from apps.core.forms import BootstrapFormMixin

from .models import ContactMessage


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, required=False)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (getattr(settings, "RECAPTCHA_PUBLIC_KEY", "") and getattr(settings, "RECAPTCHA_PRIVATE_KEY", "")):
            self.fields.pop("captcha", None)

