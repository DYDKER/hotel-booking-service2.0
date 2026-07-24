from decimal import Decimal

import pytest

from hotels.models import Room


@pytest.mark.django_db
def test_create_room_returns_room_id(client):
    payload = {
        "description": "Room 1",
        "price_per_night": "1500.00",
    }

    response = client.post("/rooms/create", data=payload)

    assert response.status_code == 201
    data = response.json()
    assert "room_id" in data

    room = Room.objects.get(id=data["room_id"])
    assert room.description == payload["description"]
    assert room.price_per_night == Decimal(payload["price_per_night"])