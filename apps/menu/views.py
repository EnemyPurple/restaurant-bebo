from __future__ import annotations

from django.core.cache import cache
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, render

from .models import Category, Dish


def menu_page(request):
    categories = cache.get("menu:categories")
    if categories is None:
        categories = list(
            Category.objects.filter(is_active=True)
            .annotate(
                is_drink=Case(
                    When(name__icontains="напит", then=Value(1)),
                    When(slug__in=["drinks", "drink", "beverages", "beverage", "napitki"], then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by("is_drink", "sort_order", "name")
        )
        cache.set("menu:categories", categories, 60 * 5)
    return render(request, "menu/menu.html", {"categories": categories})


def dish_detail(request, slug: str):
    dish = get_object_or_404(Dish.objects.select_related("category"), slug=slug, is_active=True)
    return render(request, "menu/dish_detail.html", {"dish": dish})

