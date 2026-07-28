from datetime import date
from decimal import Decimal

import pytest

from hotels.models import Booking, Room


@pytest.mark.django_db
def test_booking_create_booking_api(client):
    room = Room.objects.create(description="Room 1", price_per_night=Decimal("1000.00"))
    payload = {
        "room_id": room.id,
        "date_start": "2021-12-30",
        "date_end": "2022-01-02",
    }
    response = client.post("/bookings/create", data=payload)
    assert response.status_code == 201
    data = response.json()
    assert "booking_id" in data
    booking = Booking.objects.get(id=data["booking_id"])
    assert booking.room == room
    assert booking.date_start == date(2021, 12, 30)
    assert booking.date_end == date(2022, 1, 2)


@pytest.mark.django_db
def test_create_booking_returns_error_for_unknown_room(client):
    payload = {
        "room_id": 999,
        "date_start": "2021-12-30",
        "date_end": "2022-01-02",
    }
    response = client.post("/bookings/create", data=payload)
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_create_booking_rejects_invalid_date_start(client):
    room = Room.objects.create(description="Room 1", price_per_night=Decimal("1000.00"))
    payload = {
        "room_id": room.id,
        "date_start": "bad date",
        "date_end": "2022-01-02",
    }
    response = client.post("/bookings/create", data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_create_booking_rejects_invalid_date_end(client):
    room = Room.objects.create(description="Room 1", price_per_night=Decimal("1000.00"))
    payload = {
        "room_id": room.id,
        "date_start": "2021-12-30",
        "date_end": "bad date",
    }
    response = client.post("/bookings/create", data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_create_booking_rejects_date_end_before_date_start(client):
    room = Room.objects.create(description="Room 1", price_per_night=Decimal("1000.00"))
    payload = {
        "room_id": room.id,
        "date_start": "2022-01-02",
        "date_end": "2021-12-30",
    }
    response = client.post("/bookings/create", data=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert Booking.objects.count() == 0

