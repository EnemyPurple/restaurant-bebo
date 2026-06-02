from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model

from apps.core.forms import BootstrapFormMixin

from apps.booking.models import Booking

from .models import Review

User = get_user_model()


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ReviewCreateForm(BootstrapFormMixin, forms.ModelForm):
    photos = forms.FileField(widget=MultiFileInput(attrs={"multiple": True}), required=False)

    class Meta:
        model = Review
        fields = ["booking", "rating", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, user: User, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["booking"].queryset = (
            Booking.objects.filter(user=user, status=Booking.Status.CONFIRMED).order_by("-date", "-time")
        )

