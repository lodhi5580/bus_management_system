from django.contrib.auth.models import User
from django.db import models


class Bus(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True)
    bus_no = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.name}"


class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.source} - {self.arrival_time} to {self.destination} - {self.departure_time}"


class RouteBusMap(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    ticket_price = models.FloatField(null=True, blank=True)

    def seats_booked(self, no_seats):
        if isinstance(no_seats, str):
            no_seats = int(no_seats)
        self.available_seats = self.available_seats - no_seats
        if self.available_seats < 0:
            return False
        self.save()
        return True

    def __str__(self):
        return f"{self.bus.name} - {self.route.source} - {self.route.destination}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(RouteBusMap, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return f"Ticket {self.id} for {self.user.username}"
