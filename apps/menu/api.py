from __future__ import annotations

from django.db.models import Case, IntegerField, Value, When
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dish


class DishListApiView(APIView):
    def get(self, request):
        category = request.query_params.get("category")
        q = request.query_params.get("q")

        qs = (
            Dish.objects.filter(is_active=True)
            .select_related("category")
            .annotate(
                category_is_drink=Case(
                    When(category__name__icontains="напит", then=Value(1)),
                    When(
                        category__slug__in=["drinks", "drink", "beverages", "beverage", "napitki"],
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by("category_is_drink", "category__sort_order", "category__name", "name")
        )
        if category:
            qs = qs.filter(category__slug=category)
        if q:
            qs = qs.filter(name__icontains=q)

        data = [
            {
                "id": d.id,
                "name": d.name,
                "slug": d.slug,
                "category": {"name": d.category.name, "slug": d.category.slug},
                "description": d.description,
                "price": str(d.price),
                "weight": d.weight,
                "photo": d.photo.url if d.photo else "",
                "is_spicy": d.is_spicy,
                "is_vegetarian": d.is_vegetarian,
                "is_recommended": d.is_recommended,
                "allergens": d.allergens,
            }
            for d in qs[:500]
        ]
        return Response({"results": data})

