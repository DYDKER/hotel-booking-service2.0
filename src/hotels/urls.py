from django.urls import path

from hotels.views import create_booking, create_room, delete_room, list_rooms

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
    path("rooms/list", list_rooms, name="room_list"),
    path("rooms/delete", delete_room, name="delete_room"),
    path("bookings/create", create_booking, name="create_booking"),
]