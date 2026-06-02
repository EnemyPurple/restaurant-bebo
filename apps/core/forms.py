from __future__ import annotations

from django import forms


def _append_class(attrs: dict, class_name: str) -> None:
    existing = attrs.get("class", "")
    classes = existing.split()
    if class_name not in classes:
        attrs["class"] = f"{existing} {class_name}".strip()


class BootstrapFormMixin:
    """Добавляет Bootstrap-классы ко всем видимым полям формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_field_styles()

    def _apply_bootstrap_field_styles(self) -> None:
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.HiddenInput):
                continue
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                _append_class(widget.attrs, "form-select")
            elif isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                _append_class(widget.attrs, "form-check-input")
            else:
                _append_class(widget.attrs, "form-control")
