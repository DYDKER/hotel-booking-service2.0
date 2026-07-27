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


@pytest.mark.django_db
def test_create_room_rejects_empty_description(client):
    payload = {
        "description": "",
        "price_per_night": "1500.00",
    }

    response = client.post("/rooms/create", data=payload)

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_create_room_rejects_non_positive_price(client):
    payload = {
        "description": "Room 1",
        "price_per_night": "0.00",
    }

    response = client.post("/rooms/create", data=payload)

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert Room.objects.count() == 0


@pytest.mark.django_db
def test_get_room_list_returns_created_rooms(client):
    Room.objects.create(description="Room 1", price_per_night=Decimal("1000.00"))
    Room.objects.create(description="Room 2", price_per_night=Decimal("2000.00"))
    response = client.get("/rooms/list")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    descriptions = [room["description"] for room in data]
    assert "Room 1" in descriptions
    assert "Room 2" in descriptions


@pytest.mark.django_db
def test_get_room_list_returns_sorted_by_price_asc(client):
    Room.objects.create(description="Expensive room", price_per_night=Decimal("3000.00"))
    Room.objects.create(description="Cheap room", price_per_night=Decimal("1000.00"))
    response = client.get("/rooms/list?sort=price&order=asc")
    data = response.json()
    descriptions = [room["description"] for room in data]
    assert descriptions == ["Cheap room", "Expensive room"]


@pytest.mark.django_db
def test_get_room_list_returns_sorted_by_price_desc(client):
    Room.objects.create(description="Cheap room", price_per_night=Decimal("1000.00"))
    Room.objects.create(description="Expensive room", price_per_night=Decimal("3000.00"))
    response = client.get("/rooms/list?sort=price&order=desc")
    data = response.json()
    descriptions = [room["description"] for room in data]
    assert descriptions == ["Expensive room", "Cheap room"]


@pytest.mark.django_db
def test_get_room_list_returns_sorted_by_created_at_desc(client):
    Room.objects.create(description="First room", price_per_night=Decimal("1000.00"))
    Room.objects.create(description="Second room", price_per_night=Decimal("3000.00"))
    response = client.get("/rooms/list?sort=created_at&order=desc")
    data = response.json()
    descriptions = [room["description"] for room in data]
    assert descriptions == ["Second room", "First room"]


@pytest.mark.django_db
def test_get_room_list_returns_sorted_by_created_at_asc(client):
    Room.objects.create(description="First room", price_per_night=Decimal("1000.00"))
    Room.objects.create(description="Second room", price_per_night=Decimal("3000.00"))
    response = client.get("/rooms/list?sort=created_at&order=asc")
    data = response.json()
    descriptions = [room["description"] for room in data]
    assert descriptions == ["First room", "Second room"]


@pytest.mark.django_db
def test_delete_room_removes_existing_room(client):
    room = Room.objects.create(description="First room", price_per_night=Decimal("1000.00"))
    response = client.post("/rooms/delete", data={"room_id": room.id})
    assert response.status_code == 200
    assert Room.objects.count() == 0
    data = response.json()
    assert data["deleted"] is True


@pytest.mark.django_db
def test_delete_room_returns_error_for_unknown_room(client):
    response = client.post("/rooms/delete", data={"room_id": 999})

    assert response.status_code == 404
    data = response.json()
    assert "error" in data