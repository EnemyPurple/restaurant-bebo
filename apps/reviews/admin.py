from django.contrib import admin

from .models import Review, ReviewPhoto


class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_published", "created_at", "booking", "user")
    list_filter = ("is_published", "rating")
    search_fields = ("name", "text")
    list_editable = ("is_published",)
    readonly_fields = ("created_at",)
    inlines = [ReviewPhotoInline]

