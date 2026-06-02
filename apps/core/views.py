from django.shortcuts import render
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from apps.events.models import Event
from apps.menu.models import Dish
from apps.reviews.models import Review


def home(request):
    reviews = Review.objects.filter(is_published=True).order_by("-created_at")[:6]
    events = Event.objects.filter(is_published=True).order_by("date_start")[:3]
    upcoming_event = Event.objects.filter(is_published=True, date_start__gte=timezone.now()).order_by("date_start").first()
    dishes = (
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
    )
    ordered_dishes = dishes.order_by("category_is_drink", "category__sort_order", "name")
    dish_of_day = ordered_dishes.filter(is_recommended=True).first() or ordered_dishes.first()
    chef_picks_qs = ordered_dishes.exclude(pk=getattr(dish_of_day, "pk", None)).order_by(
        "category_is_drink", "-is_recommended", "category__sort_order", "name"
    )
    chef_picks = list(chef_picks_qs[:6])
    return render(
        request,
        "core/home.html",
        {
            "reviews": reviews,
            "events": events,
            "upcoming_event": upcoming_event,
            "dish_of_day": dish_of_day,
            "chef_picks": chef_picks,
        },
    )

