from django.http import JsonResponse
from django.views.decorators.http import require_POST

from hotels import services


@require_POST
def create_room(request):
    description = request.POST.get("description")
    price_per_night = request.POST.get("price_per_night")
    room = services.create_room(description=description, price_per_night=price_per_night)
    return JsonResponse({"room_id": room.id}, status=201)