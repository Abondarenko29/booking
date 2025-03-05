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
            bookings = Booking.objects.filter(room=room)

        except Room.DoesNotExist:
            return HttpResponse("Room doesn't exist.",
                                status=404)

        conditionals = []
        booking = Booking(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time,
            )
        for booking_is_be in bookings:
            conditional1 = (booking.end_time
                            <= str(booking_is_be.start_time))
            conditional2 = (booking.start_time
                            >= str(booking_is_be.end_time))
            conditionals.append(conditional1 or conditional2)

        conditional = booking.end_time > booking.start_time
        if not (False in conditionals) and conditional:
            booking.save()
            return redirect('booking-details', pk=booking.id)

        elif not (conditional):
            return HttpResponse("""Кінцева дата повинна
                                бути більшою за початкову""",
                                status=404)

        else:
            return HttpResponse("На цей час вже забронювали, виберіть інший.",
                                status=404)

    else:
        default_room_number = request.GET.get("room-number")
        default_room_number = str(default_room_number)
        default_room_number = default_room_number.replace("None", "")
        context = {
            "room_number": default_room_number,
        }
        return render(request,
                      "booking/booking_form.html",
                      context)


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
