from hotels.models import Room


def create_room(description: str, price_per_night: str) -> Room:
    room = Room.objects.create(description=description, price_per_night=price_per_night)
    return room