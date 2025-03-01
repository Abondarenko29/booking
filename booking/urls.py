from django.urls import path
from .views import room_list, room_details, book_room, booking_details
from .views import booking_list


urlpatterns = [
    path("", room_list, name="room-list"),
    path("<int:pk>", room_details, name="room-details"),
    path("book-room/", book_room, name="book-room"),
    path("booking/<int:pk>/", booking_details, name="booking-details"),
    path("bookings/", booking_list, name="booking-list"),
]
