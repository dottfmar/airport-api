from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    AirplaneType,
    Airplane,
    Crew,
    Airport,
    Route,
    Flight,
    Ticket,
    Order,
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = [
            "id",
            "name",
        ]


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ["id", "image"]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "total_number_of_seats",
            "image",
        ]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.StringRelatedField(
        source="airplane_type.name", read_only=True
    )

    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "airplane_type",
            "total_number_of_seats",
        ]


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Crew.Roles.choices)

    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
            "role",
            "full_name",
        ]


class CrewListSerializer(CrewSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            "id",
            "full_name",
            "role",
        ]

    def get_role(self, obj):
        return obj.get_role_display()


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "city",
            "country",
            "latitude",
            "longitude",
        ]


class AirportListSerializer(AirportSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "city",
            "country",
        ]


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all(),
        read_only=False,
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all(),
        read_only=False,
    )

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteDetailSerializer(RouteSerializer):
    source = AirportListSerializer(read_only=True)
    destination = AirportListSerializer(read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        queryset=Route.objects.all().select_related("source", "destination"),
        slug_field="id",
    )
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all().select_related("airplane_type"),
    )
    crew = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(),
        many=True
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        ]

    def create(self, validated_data):
        crew_data = validated_data.pop("crew")
        flight = Flight.objects.create(**validated_data)
        flight.crew.set(crew_data)
        self.validate_crew_availability(flight)
        return flight

    def update(self, instance, validated_data):
        crew_data = validated_data.pop("crew", None)
        instance = super().update(instance, validated_data)
        if crew_data is not None:
            instance.crew.set(crew_data)
        self.validate_crew_availability(instance)
        return instance

    def validate_crew_availability(self, flight):
        overlapping_flights = Flight.objects.filter(
            Q(
                departure_time__lt=flight.arrival_time,
                arrival_time__gt=flight.departure_time,
            )
        ).exclude(id=flight.id)

        for crew_member in flight.crew.all():
            busy_crew = overlapping_flights.filter(crew=crew_member)
            if busy_crew.exists():
                raise ValidationError(
                    "Some crew members is already assigned"
                    " to another flight during this time."
                )


class FlightListSerializer(FlightSerializer):
    crew = CrewListSerializer(read_only=True, many=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        route = instance.route
        formatted_route = (
            f"{route.source.city} ({route.source.country})"
            f" -> {route.destination.city} "
            f"({route.destination.country})"
        )
        representation["route"] = formatted_route
        return representation


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crew = CrewSerializer(read_only=True, many=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "seat",
            "row",
            "flight",
        ]

    def validate(self, attrs):
        Ticket.validate_value(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            "Invalid seat number",
            serializers.ValidationError,
        )

        Ticket.validate_value(
            attrs["row"],
            attrs["flight"].airplane.rows,
            "Invalid row number",
            serializers.ValidationError,
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "tickets",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order
