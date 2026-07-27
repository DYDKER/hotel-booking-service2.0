from django.urls import path

from hotels.views import create_room, list_rooms

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
    path("rooms/list", list_rooms, name="room_list"),
]