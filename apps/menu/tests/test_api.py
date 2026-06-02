import pytest
from django.urls import reverse

from apps.menu.models import Category, Dish


@pytest.mark.django_db
def test_menu_api_filters_by_category(client):
    c1 = Category.objects.create(name="Салаты", slug="salads")
    c2 = Category.objects.create(name="Десерты", slug="desserts")
    Dish.objects.create(category=c1, name="Цезарь", slug="caesar", price="500.00", weight=200)
    Dish.objects.create(category=c2, name="Наполеон", slug="napoleon", price="350.00", weight=150)

    url = reverse("api_dishes") + "?category=salads"
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()["results"]
    assert len(data) == 1
    assert data[0]["slug"] == "caesar"


@pytest.mark.django_db
def test_menu_api_shows_dishes_before_drinks(client):
    drinks = Category.objects.create(name="Напитки", slug="drinks", sort_order=1)
    dishes = Category.objects.create(name="Закуски", slug="snacks", sort_order=2)
    Dish.objects.create(category=drinks, name="Лимонад", slug="lemonade", price="300.00", weight=300)
    Dish.objects.create(category=dishes, name="Хачапури", slug="hachapuri", price="600.00", weight=350)

    resp = client.get(reverse("api_dishes"))
    assert resp.status_code == 200
    data = resp.json()["results"]
    assert [item["slug"] for item in data] == ["hachapuri", "lemonade"]

