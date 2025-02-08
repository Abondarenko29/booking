from django.shortcuts import render
from .models import Room, Booking


def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
        }
    return render(request,
                  "booking/room_list.html",
                  context)
