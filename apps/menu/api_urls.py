from django.urls import path

from . import api

urlpatterns = [
    path("dishes/", api.DishListApiView.as_view(), name="api_dishes"),
]

