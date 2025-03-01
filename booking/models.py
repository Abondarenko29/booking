from django.db import models
from django.conf import settings


# Create your models here.
class Room(models.Model):
    number = models.CharField(max_length=5)
    capacity = models.PositiveIntegerField()
    # image = models.ImageField()
    location = models.CharField(max_length=3900)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(blank=True, null=True)
    area = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.number} at {self.capacity}"

    class Meta:
        verbose_name = "room"
        verbose_name_plural = "rooms"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="booking")
    room = models.ForeignKey(Room, on_delete=models.SET("1"),
                             related_name="room")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} books {self.room}"

    class Meta:
        verbose_name = "booking"
        verbose_name_plural = "bookings"
