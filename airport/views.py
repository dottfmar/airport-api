from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response

from airport import examples_swagger
from airport.models import Airplane, Crew, Airport, Route, Flight, Order
from airport.serializers import (
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    CrewSerializer,
    CrewListSerializer,
    AirportSerializer,
    AirportListSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    AirplaneImageSerializer,
)


class ObjectPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "per_page"
    max_page_size = 10


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = ObjectPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()

        if name := self.request.query_params.get("name"):
            queryset = queryset.filter(name__icontains=name)
        if seats_in_row := self.request.query_params.get("seats_in_row"):
            queryset = queryset.filter(seats_in_row=int(seats_in_row))
        if rows := self.request.query_params.get("rows"):
            queryset = queryset.filter(rows=int(rows))
        if airplane_type := self.request.query_params.get("airplane_type"):
            queryset = queryset.filter(
                airplane_type__name__in=airplane_type.split(",")
            )

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific airplane"""
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()

        if first_name := self.request.query_params.get("first_name"):
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name := self.request.query_params.get("last_name"):
            queryset = queryset.filter(last_name__icontains=last_name)
        if role := self.request.query_params.get("role"):
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

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()

        if name := self.request.query_params.get("name"):
            queryset = queryset.filter(name__icontains=name)
        if country := self.request.query_params.get("country"):
            queryset = queryset.filter(country__in=country.split(","))
        if city := self.request.query_params.get("city"):
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
    queryset = Route.objects.all()
    pagination_class = ObjectPagination
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        return super().get_serializer_class()


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = ObjectPagination

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return super().get_serializer_class()

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = super().get_queryset()

        if routes := self.request.query_params.get("routes"):
            routes_ids = self._params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)

        if airplanes := self.request.GET.get("airplanes"):
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
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
