from django.urls import path

from hotels.views import (
    create_booking,
    create_room,
    delete_booking,
    delete_room,
    list_bookings,
    list_rooms,
)

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
    path("rooms/list", list_rooms, name="room_list"),
    path("rooms/delete", delete_room, name="delete_room"),
    path("bookings/create", create_booking, name="create_booking"),
    path("bookings/delete", delete_booking, name="delete_booking"),
    path("bookings/list", list_bookings, name="list_bookings"),
]