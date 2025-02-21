from rest_framework import viewsets, filters

from airport.models import Airplane
from airport.serializers import AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "total_number_of_seats"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer
