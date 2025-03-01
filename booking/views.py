from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Booking
from django.contrib.auth.decorators import login_required


def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
        }
    return render(request,
                  "booking/room_list.html",
                  context)


def room_details(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        "room": room,
        }
    return render(request,
                  "booking/room_details.html",
                  context)


@login_required
def book_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room-number")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            room = Room.objects.get(number=room_number)

        except Room.DoesNotExist:
            return HttpResponse("Room doesn't exist.",
                                status=404)

        booking = Booking.objects.create(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time,
            )
        return redirect('booking-details', pk=booking.id)

    else:
        return render(request,
                      "booking/booking_form.html",)


def booking_details(request, pk):
    booking = Booking.objects.get(id=pk)
    days = (booking.end_time - booking.start_time).days
    total = days * booking.room.price
    context = {
        "booking": booking,
        "total": total,
        }
    return render(request,
                  "booking/booking_details.html",
                  context)


@login_required(login_url="login")
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    # total = list(map(calculate_total, bookings))

    context = {
        "bookings": bookings,
    }
    return render(
        request,
        "booking/booking_list.html",
        context
    )
