from django.urls import path

from . import api

urlpatterns = [
    path("availability/", api.AvailabilityApiView.as_view(), name="availability"),
]

