from django.urls import include, path

urlpatterns = [
    path("menu/", include("apps.menu.api_urls")),
    path("booking/", include("apps.booking.api_urls")),
]

