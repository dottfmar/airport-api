from rest_framework import viewsets, filters

from airport.models import Airplane
from airport.serializers import AirplaneSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "total_number_of_seats"]
    ordering = ["name"]
