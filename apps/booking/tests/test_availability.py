import pytest
from django.urls import reverse

from apps.booking.models import Booking, Table


@pytest.mark.django_db
def test_availability_excludes_busy_table(client):
    t1 = Table.objects.create(number=1, seats=2, location="hall", is_active=True)
    t2 = Table.objects.create(number=2, seats=4, location="hall", is_active=True)
    Booking.objects.create(
        name="A",
        phone="+70000000000",
        email="a@example.com",
        table=t2,
        date="2026-03-17",
        time="19:00",
        guests=2,
        status=Booking.Status.CONFIRMED,
    )
    url = reverse("availability") + "?date=2026-03-17&time=19:00&guests=2"
    resp = client.get(url)
    assert resp.status_code == 200
    ids = [x["id"] for x in resp.json()["results"]]
    assert t1.id in ids
    assert t2.id not in ids

