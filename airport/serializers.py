from rest_framework import serializers

from airport.models import AirplaneType, Airplane, Crew


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

class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Crew.Roles.choices, source="get_role_display")
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
    class Meta:
        model = Crew
        fields = [
            "id",
            "full_name",
            "role",
        ]
