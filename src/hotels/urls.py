from django.urls import path

from hotels.views import create_room

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
]