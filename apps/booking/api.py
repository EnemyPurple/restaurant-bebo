from __future__ import annotations

from datetime import date as date_type
from datetime import time as time_type

from django.db.models import Q
from django.utils.dateparse import parse_date, parse_time
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Table


class AvailabilityApiView(APIView):
    def get(self, request):
        date_s = request.query_params.get("date")
        time_s = request.query_params.get("time")
        guests_s = request.query_params.get("guests")

        date_v: date_type | None = parse_date(date_s) if date_s else None
        time_v: time_type | None = parse_time(time_s) if time_s else None
        guests = int(guests_s) if guests_s and guests_s.isdigit() else None

        if not date_v or not time_v or not guests:
            return Response({"error": "date, time, guests are required"}, status=400)

        tables = Table.objects.filter(is_active=True, seats__gte=guests)
        busy_table_ids = Booking.objects.filter(
            Q(status=Booking.Status.PENDING) | Q(status=Booking.Status.CONFIRMED),
            date=date_v,
            time=time_v,
        ).values_list("table_id", flat=True)

        available = tables.exclude(id__in=list(busy_table_ids)).order_by("seats", "number")[:50]
        return Response(
            {
                "results": [
                    {"id": t.id, "number": t.number, "seats": t.seats, "location": t.location} for t in available
                ]
            }
        )

