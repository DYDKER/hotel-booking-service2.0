from django.urls import path

from hotels.views import (
    BookingCollectionView,
    BookingDetailView,
    RoomBookingListView,
    RoomCollectionView,
    RoomDetailView,
)

urlpatterns = [
    path("rooms/", RoomCollectionView.as_view(), name="room_collection"),
    path("rooms/<int:room_id>/", RoomDetailView.as_view(), name="room_detail"),
    path("rooms/<int:room_id>/bookings/", RoomBookingListView.as_view(), name="room_booking_list"),
    path("bookings/", BookingCollectionView.as_view(), name="booking_collection"),
    path("bookings/<int:booking_id>/", BookingDetailView.as_view(), name="booking_detail"),
]