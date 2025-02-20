from math import radians, sin, cos, atan2, sqrt

from django.db import models

from airport_service import settings


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    @property
    def total_number_of_seats(self):
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, (type: {self.airplane_type.name})"

class Crew(models.Model):

    class Roles(models.TextChoices):
        CAPTAIN = "CAPTAIN", "Pilot in Command"
        SECOND_PILOT = "SECOND_PILOT", "Co-Pilot"
        STEWARD = "STEWARD", "Flight Attendant"
        OTHER = "OTHER", "Other staff"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(choices=Roles, max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}, {self.get_role_display()}"


class Flight(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self):
        return f"Flight: {self.route}, airplane: {self.airplane}"

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def calculate_distance(self, airport):
        ...

    def __str__(self):
        return f"Airport: {self.name}, city: {self.city}, country: {self.country}"

class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="destination")

    @property
    def distance(self):
        return self.source.calculate_distance(self.destination) if self.source and self.destination else None

    def __str__(self):
        return f"{self.source.city} ({self.source.country}) -> {self.destination.city} ({self.destination.country})"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["row", "seat", "flight"]

    def __str__(self):
        return f"Ticket: {self.flight}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

