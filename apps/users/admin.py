from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import OperationLog, PhoneOTP, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("phone", "full_name", "email", "birthday", "visits_count", "total_spent", "discount_percent")
    search_fields = ("phone", "full_name", "email")
    readonly_fields = ("created_at", "updated_at", "discount_percent", "auto_discount_percent", "orders_history_link")
    fieldsets = (
        (None, {"fields": ("user", "phone", "full_name", "email", "birthday")}),
        (
            "Скидка и статистика",
            {"fields": ("visits_count", "total_spent", "auto_discount_percent", "manual_discount_percent", "discount_percent")},
        ),
        ("История", {"fields": ("orders_history_link",)}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="История заказов (бронирований)")
    def orders_history_link(self, obj: Profile):
        if not obj.user_id:
            return "—"
        url = reverse("admin:booking_booking_changelist") + f"?user__id__exact={obj.user_id}"
        return format_html('<a href="{}">Открыть бронирования пользователя</a>', url)


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at", "expires_at", "attempts_left", "is_used")
    list_filter = ("is_used",)
    search_fields = ("phone", "code")
    readonly_fields = ("created_at",)


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ("user", "kind", "amount", "percent", "created_at")
    list_filter = ("kind",)
    search_fields = ("user__username", "description")
    readonly_fields = ("created_at",)

