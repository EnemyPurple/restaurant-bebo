from django.contrib import admin

from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "is_recommended", "is_spicy", "is_vegetarian")
    list_filter = ("is_active", "category", "is_recommended", "is_spicy", "is_vegetarian")
    list_editable = ("is_active", "is_recommended", "is_spicy", "is_vegetarian")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}

