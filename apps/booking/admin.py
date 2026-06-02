from django.contrib import admin

from .models import Booking, Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats", "location", "is_active")
    list_editable = ("seats", "location", "is_active")
    list_filter = ("location", "is_active")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "table", "guests", "name", "phone", "status", "spent_amount", "is_visit_counted", "created_at")
    list_filter = ("status", "date", "table", "is_visit_counted")
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at",)

