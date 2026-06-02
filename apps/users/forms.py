from __future__ import annotations

import re

from django import forms
from apps.core.forms import BootstrapFormMixin

from django.core.exceptions import ValidationError

PHONE_RE = re.compile(r"^\+?\d[\d\-\s\(\)]{7,}$")


class PhoneLoginRequestForm(BootstrapFormMixin, forms.Form):
    phone = forms.CharField(max_length=32, widget=forms.TextInput(attrs={"placeholder": "+7 900 000-00-00"}))

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not PHONE_RE.match(phone):
            raise ValidationError("Введите корректный номер телефона.")
        return phone


class PhoneLoginVerifyForm(BootstrapFormMixin, forms.Form):
    phone = forms.CharField(max_length=32, widget=forms.HiddenInput())
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"placeholder": "Код из SMS"}))

    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip()
        if not (code.isdigit() and len(code) == 6):
            raise ValidationError("Код должен состоять из 6 цифр.")
        return code


class ProfileRegistrationForm(BootstrapFormMixin, forms.Form):
    full_name = forms.CharField(max_length=200, required=False, label="Имя")
    email = forms.EmailField(required=False, label="Email")
    birthday = forms.DateField(required=False, label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"}))

