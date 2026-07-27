from decimal import Decimal

from hotels.models import Room


class RoomValidationError(Exception):
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
