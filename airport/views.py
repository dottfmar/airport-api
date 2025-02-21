from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from airport.models import Airplane, Crew, Airport, Route, Flight
from airport.serializers import AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer, CrewSerializer, \
    CrewListSerializer, AirportSerializer, AirportListSerializer, RouteSerializer, RouteDetailSerializer, \
    FlightListSerializer


class ObjectPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'
    max_page_size = 10


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    pagination_class = ObjectPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = ObjectPagination

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        return CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = ObjectPagination

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        return AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = ObjectPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


