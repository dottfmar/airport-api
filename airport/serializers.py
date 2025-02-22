from rest_framework import serializers

from airport.models import AirplaneType, Airplane, Crew, Airport, Route, Flight


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = [
            "id",
            "name",
        ]


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
        ]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.StringRelatedField(
        source="airplane_type.name",
        read_only=True
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
        fields = [
            "id",
            "source",
            "destination",
            "distance"
        ]

class RouteDetailSerializer(RouteSerializer):
    source = AirportListSerializer(read_only=True)
    destination = AirportListSerializer(read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        queryset=Route.objects.all(),
        slug_field="id",
    )
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all(),
    )
    crew = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), many=True)

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
        formatted_route = f"{route.source.city} ({route.source.country}) -> {route.destination.city} ({route.destination.country})"
        representation['route'] = formatted_route
        return representation

    def create(self, validated_data):
        crew_data = validated_data.pop('crew')
        flight = Flight.objects.create(**validated_data)
        flight.crew.set(crew_data)
        return flight

    def update(self, instance, validated_data):
        crew_data = validated_data.pop('crew', None)
        instance = super().update(instance, validated_data)
        if crew_data is not None:
            instance.crew.set(crew_data)
        return instance

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