from datetime import date
from decimal import Decimal

from hotels.models import Booking, Room


class RoomValidationError(Exception):
    pass


class RoomNotFound(Exception):
    pass


class BookingValidationError(Exception):
    pass


def create_room(description: str, price_per_night: str) -> Room:
    if description is None or description.strip() == "":
        raise RoomValidationError("description is required")
    price_per_night = Decimal(price_per_night)
    if price_per_night <= 0:
        raise RoomValidationError("price_per_night must be greater than 0")
    return Room.objects.create(description=description, price_per_night=price_per_night)


def list_rooms(sort=None, order="asc"):
    rooms = Room.objects.all()

    sort_fields = {
        "price": "price_per_night",
        "created_at": "created_at",
    }
    if sort in sort_fields:
        ordering = sort_fields[sort]
        if order == "desc":
            ordering = "-" + ordering
        rooms = rooms.order_by(ordering)
    return rooms


def delete_room(room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise RoomNotFound("room not found") from None
    room.delete()


def create_booking(room_id: str, date_start: date, date_end: date) -> Booking:
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise RoomNotFound("room not found") from None
    try:
        parsed_date_start = date.fromisoformat(date_start)
        parsed_date_end = date.fromisoformat(date_end)
    except ValueError:
        raise BookingValidationError("invalid date format") from None
    if parsed_date_end < parsed_date_start:
        raise BookingValidationError(
            "date_end must be greater than or equal to date_start"
        ) from None
    booking = Booking.objects.create(
        room=room,
        date_start=parsed_date_start,
        date_end=parsed_date_end,
    )
    return booking
