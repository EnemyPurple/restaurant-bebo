from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
    path("", views.newsletter_page, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
]

