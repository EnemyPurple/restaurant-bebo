from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.phone_login_request, name="login"),
    path("login/verify/", views.phone_login_verify, name="login_verify"),
    path("register/", views.register_profile, name="register"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.cabinet, name="cabinet"),
]

