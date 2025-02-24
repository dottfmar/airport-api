from django.template.defaultfilters import first
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from airport import examples_swagger
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.models import Airplane, Crew, Airport, Route, Flight, Order
from airport.serializers import AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer, CrewSerializer, \
    CrewListSerializer, AirportSerializer, AirportListSerializer, RouteSerializer, RouteDetailSerializer, \
    FlightSerializer, FlightListSerializer, FlightDetailSerializer, OrderSerializer


class ObjectPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'
    max_page_size = 10


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    pagination_class = ObjectPagination
    filter_backends = [filters.OrderingFilter]
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        seats_in_row = self.request.query_params.get("seats_in_row")
        rows = self.request.query_params.get("rows")
        airplane_type = self.request.query_params.get("airplane_type")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if seats_in_row:
            queryset = queryset.filter(seats_in_row=int(seats_in_row))
        if rows:
            queryset = queryset.filter(rows=int(rows))
        if airplane_type:
            queryset = queryset.filter(airplane_type__name__in=airplane_type.split(","))

        return queryset.distinct()

    @extend_schema(
        parameters=examples_swagger.airplane_get_parameters,
        responses=examples_swagger.airplane_get_responses,
    )
    def list(self, request, *args, **kwargs):
        """Retrieve a list of airplanes with optional filters."""
        return super().list(request, *args, **kwargs)

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = ObjectPagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        return CrewSerializer

    def get_queryset(self):
        queryset = self.queryset

        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        role = self.request.query_params.get("role")

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if role:
            if role in Crew.Roles:
                queryset = queryset.filter(role=role)
            else:
                queryset = queryset.none()

        return queryset.distinct()

    @extend_schema(
        parameters=examples_swagger.crew_get_parameters,
        responses=examples_swagger.crew_get_responses,
    )
    def list(self, request, *args, **kwargs):
        """Retrieve a list of crews with optional filters."""
        return super().list(request, *args, **kwargs)

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = ObjectPagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        return AirportSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country = self.request.query_params.get("country")
        city = self.request.query_params.get("city")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if country:
            queryset = queryset.filter(country__in=country.split(","))
        if city:
            queryset = queryset.filter(city__in=city.split(","))

        return queryset.distinct()

    @extend_schema(
        parameters=examples_swagger.airport_get_parameters,
        responses=examples_swagger.airport_get_responses,
    )
    def list(self, request, *args, **kwargs):
        """Retrieve a list of airports with optional filters."""
        return super().list(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related()
    serializer_class = RouteSerializer
    pagination_class = ObjectPagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.prefetch_related("crew").select_related("airplane").select_related("route")
    serializer_class = FlightSerializer
    pagination_class = ObjectPagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        routes = self.request.query_params.get("routes")
        airplanes = self.request.GET.get("airplanes")

        if routes:
            routes_ids = self._params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)

        if airplanes:
            queryset = queryset.filter(airplane__name__in=airplanes.split(","))

        return queryset.distinct()

    @extend_schema(
        parameters=examples_swagger.flight_get_parameters,
        responses=examples_swagger.flight_get_responses,
    )
    def list(self, request, *args, **kwargs):
        """Retrieve a list of flights with optional filters."""
        return super().list(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ObjectPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
