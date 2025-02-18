# railway/models.py
from django.db import models
from django.contrib.auth.models import User

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}: {self.source} -> {self.destination}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on train {self.train.name}"
