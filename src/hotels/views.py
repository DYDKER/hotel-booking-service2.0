from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from hotels import services


@method_decorator(csrf_exempt, name="dispatch")
class RoomCollectionView(View):
    def get(self, request):
        sort = request.GET.get("sort")
        order = request.GET.get("order", "asc")

        rooms = services.list_rooms(sort=sort, order=order)
        data = [
            {
                "room_id": room.id,
                "description": room.description,
                "price_per_night": str(room.price_per_night),
                "created_at": room.created_at.isoformat(),
            }
            for room in rooms
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        description = request.POST.get("description")
        price_per_night = request.POST.get("price_per_night")
        try:
            room = services.create_room(
                description=description,
                price_per_night=price_per_night,
            )
        except services.RoomValidationError as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse({"room_id": room.id}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class RoomDetailView(View):
    def delete(self, request, room_id):
        try:
            services.delete_room(room_id=room_id)
        except services.RoomNotFound as error:
            return JsonResponse({"error": str(error)}, status=404)
        return JsonResponse({"deleted": True})


@method_decorator(csrf_exempt, name="dispatch")
class BookingCollectionView(View):
    def post(self, request):
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


@method_decorator(csrf_exempt, name="dispatch")
class BookingDetailView(View):
    def delete(self, request, booking_id):
        try:
            services.delete_booking(booking_id=booking_id)
        except services.BookingNotFound as error:
            return JsonResponse({"error": str(error)}, status=404)
        return JsonResponse({"deleted": True})


class RoomBookingListView(View):
    def get(self, request, room_id):
        try:
            bookings = services.list_bookings(room_id=room_id)
        except services.RoomNotFound as error:
            return JsonResponse({"error": str(error)}, status=404)
        data = [
            {
                "booking_id": booking.id,
                "date_start": booking.date_start.isoformat(),
                "date_end": booking.date_end.isoformat(),
            }
            for booking in bookings
        ]
        return JsonResponse(data, safe=False)
