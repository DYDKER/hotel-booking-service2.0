from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from hotels import services


@csrf_exempt
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


@csrf_exempt
@require_POST
def delete_room(request):
    room_id = request.POST.get("room_id")
    try:
        services.delete_room(room_id=room_id)
    except services.RoomNotFound as error:
        return JsonResponse({"error": str(error)}, status=404)
    return JsonResponse({"deleted": True})


@csrf_exempt
@require_POST
def create_booking(request):
    room_id = request.POST.get("room_id")
    date_start = request.POST.get("date_start")
    date_end = request.POST.get("date_end")

    try:
        booking = services.create_booking(
            room_id=room_id,
            date_start=date_start,
            date_end=date_end,
        )
    except services.RoomNotFound as error:
        return JsonResponse({"error": str(error)}, status=404)
    except services.BookingValidationError as error:
        return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"booking_id": booking.id}, status=201)


@csrf_exempt
@require_POST
def delete_booking(request):
    booking_id = request.POST.get("booking_id")
    try:
        services.delete_booking(booking_id=booking_id)
    except services.BookingNotFound as error:
        return JsonResponse({"error": str(error)}, status=404)
    return JsonResponse({"deleted": True})


@require_GET
def list_bookings(request):
    room_id = request.GET.get("room_id")
    try:
        bookings = services.list_bookings(room_id=room_id)
    except services.RoomNotFound as error:
        return JsonResponse({"error": str(error)}, status=404)
    data = []
    for booking in bookings:
        data.append({
            "booking_id": booking.id,
            "date_start": booking.date_start.isoformat(),
            "date_end": booking.date_end.isoformat(),
        })
    return JsonResponse(data, safe=False)