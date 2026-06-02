from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.events_list, name="list"),
    path("<slug:slug>/", views.event_detail, name="detail"),
    path("<slug:slug>/register/", views.register_for_event, name="register"),
    path("<slug:slug>/cancel/", views.cancel_registration, name="cancel"),
]

