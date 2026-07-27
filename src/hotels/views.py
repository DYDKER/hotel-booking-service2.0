from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from hotels import services


@require_POST
def create_room(request):
    description = request.POST.get("description")
    price_per_night = request.POST.get("price_per_night")
    try:
        room = services.create_room(description=description, price_per_night=price_per_night)
    except services.RoomValidationError as error:
        return JsonResponse({"error": str(error)}, status=400)
    return JsonResponse({"room_id": room.id}, status=201)


@require_GET
def list_rooms(request):
    sort = request.GET.get("sort")
    order = request.GET.get("order", "asc")

    rooms = services.list_rooms(sort=sort, order=order)
    data = []
    for room in rooms:
        data.append(
            {
                "room_id": room.id,
                "description": room.description,
                "price_per_night": str(room.price_per_night),
                "created_at": room.created_at.isoformat(),
            }
        )
    return JsonResponse(data, safe=False)


@require_POST
def delete_room(request):
    room_id = request.POST.get("room_id")
    try:
        services.delete_room(room_id=room_id)
    except services.RoomNotFound as error:
        return JsonResponse({"error": str(error)}, status=404)
    return JsonResponse({"deleted": True})