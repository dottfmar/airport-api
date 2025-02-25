from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from airport.models import Airport, Airplane, AirplaneType, Route, Crew, Flight
from airport.serializers import (
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirportListSerializer,
    AirportSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    CrewListSerializer,
    CrewSerializer,
)

AIRPLANE_URL = reverse("airport:airplane-list")
AIRPORT_URL = reverse("airport:airport-list")
FLIGHTS_URL = reverse("airport:flight-list")
CREW_URL = reverse("airport:crew-list")
ROUTES_URL = reverse("airport:route-list")


class UnauthenticatedAirportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(FLIGHTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def airplane_sample(**params):
    airplane_type = AirplaneType.objects.create(
        name="Test Type",
    )
    defaults = {
        "name": "Test Name",
        "seats_in_row": 5,
        "rows": 20,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def airport_sample(**params):
    defaults = {
        "name": "Test Name",
        "city": "Test City",
        "country": "Test Country",
        "latitude": 51.5007,
        "longitude": 0.1246,
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def flight_sample(**params):
    airport_1 = airport_sample()
    airport_2 = airport_sample(name="Test Airport")
    route = Route.objects.create(
        source=airport_1,
        destination=airport_2,
    )
    airplane = airplane_sample()
    departure_time = timezone.now()
    arrival_time = departure_time + timedelta(hours=2)
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)


def crew_sample(**params):
    defaults = {
        "first_name": "Alex",
        "last_name": "Johnson",
        "role": Crew.Roles.CAPTAIN,
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


class AuthenticatedAirplaneTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_get_airplanes(self):
        airplane_sample()

        response = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_airplanes_by_name(self):
        airplane_1 = airplane_sample(name="Airbus")
        airplane_2 = airplane_sample(name="Boeing")

        response = self.client.get(
            AIRPLANE_URL,
            {"name": f"{airplane_1.name}"},
        )

        serializer_airplane_1 = AirplaneListSerializer(airplane_1)
        serializer_airplane_2 = AirplaneListSerializer(airplane_2)

        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_filter_airplanes_by_seats_in_row(self):
        airplane_1 = airplane_sample(seats_in_row=5)
        airplane_2 = airplane_sample(seats_in_row=20)

        response = self.client.get(
            AIRPLANE_URL,
            {"seats_in_row": f"{airplane_1.seats_in_row}"},
        )

        serializer_airplane_1 = AirplaneListSerializer(airplane_1)
        serializer_airplane_2 = AirplaneListSerializer(airplane_2)

        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_filter_airplanes_by_rows(self):
        airplane_1 = airplane_sample(rows=20)
        airplane_2 = airplane_sample(rows=5)

        response = self.client.get(
            AIRPLANE_URL,
            {"rows": f"{airplane_1.rows}"},
        )

        serializer_airplane_1 = AirplaneListSerializer(airplane_1)
        serializer_airplane_2 = AirplaneListSerializer(airplane_2)

        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_filter_airplanes_by_airplane_type(self):
        airplane_type_1 = AirplaneType.objects.create(name="New")
        airplane_type_2 = AirplaneType.objects.create(name="Mine")

        airplane_1 = airplane_sample(airplane_type=airplane_type_1)
        airplane_2 = airplane_sample(airplane_type=airplane_type_2)

        response = self.client.get(
            AIRPLANE_URL,
            {"airplane_type": f"{airplane_type_1.name}"},
        )

        serializer_airplane_1 = AirplaneListSerializer(airplane_1)
        serializer_airplane_2 = AirplaneListSerializer(airplane_2)

        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_retrieve_airplane_by_id(self):
        airplane = airplane_sample()

        url = reverse("airport:airplane-detail", args=(airplane.id,))

        response = self.client.get(url)
        serializer = AirplaneDetailSerializer(airplane)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_forbidden(self):
        test_type = AirplaneType.objects.create(name="Test Type")
        payload = {
            "name": "Airbus",
            "rows": 20,
            "seats_in_row": 5,
            "airplane_type": test_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAirportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_get_airports(self):
        airport_sample()

        response = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer = AirportListSerializer(airports, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_airports_by_name(self):
        airport_1 = airport_sample(name="Nowhere")
        airport_2 = airport_sample(name="Somewhere")

        response = self.client.get(
            AIRPORT_URL,
            {"name": f"{airport_1.name}"},
        )

        serializer_1 = AirportListSerializer(airport_1)
        serializer_2 = AirportListSerializer(airport_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_filter_airports_by_country(self):
        airport_1 = airport_sample(country="USA")
        airport_2 = airport_sample(country="Romania")

        response = self.client.get(
            AIRPORT_URL,
            {"country": f"{airport_1.country}"},
        )

        serializer_1 = AirportListSerializer(airport_1)
        serializer_2 = AirportListSerializer(airport_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_filter_airports_by_city(self):
        airport_1 = airport_sample(city="London")
        airport_2 = airport_sample(city="Paris")

        response = self.client.get(
            AIRPORT_URL,
            {"city": f"{airport_1.city}"},
        )

        serializer_1 = AirportListSerializer(airport_1)
        serializer_2 = AirportListSerializer(airport_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_retrieve_airport_by_id(self):
        airport = airport_sample()

        url = reverse("airport:airport-detail", args=(airport.id,))

        response = self.client.get(url)
        serializer = AirportSerializer(airport)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_forbidden(self):
        payload = {
            "name": "National Airport",
            "country": "USA",
            "city": "New York",
            "latitude": 51.5007,
            "longitude": 0.1246,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedFlightsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_get_flights(self):
        flight_sample()

        response = self.client.get(FLIGHTS_URL)
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_flights_by_routes(self):
        airport_1 = airport_sample()
        airport_2 = airport_sample(name="Mine")
        airport_3 = airport_sample(name="New")
        airport_4 = airport_sample(name="Air")

        route_1 = Route.objects.create(
            source=airport_1,
            destination=airport_2,
        )
        route_2 = Route.objects.create(
            source=airport_3,
            destination=airport_4,
        )

        flight_1 = flight_sample(route=route_1)
        flight_2 = flight_sample(route=route_2)

        response = self.client.get(
            FLIGHTS_URL,
            {"routes": f"{flight_1.route.id}"},
        )

        serializer_1 = FlightListSerializer(flight_1)
        serializer_2 = FlightListSerializer(flight_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_filter_flights_by_airplanes(self):
        airplane_1 = airplane_sample(name="National Airport")
        airplane_2 = airplane_sample(name="Mine")

        flight_1 = flight_sample(airplane=airplane_1)
        flight_2 = flight_sample(airplane=airplane_2)

        response = self.client.get(
            FLIGHTS_URL,
            {"airplanes": f"{flight_1.airplane.name}"},
        )

        serializer_1 = FlightListSerializer(flight_1)
        serializer_2 = FlightListSerializer(flight_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_retrieve_flight_by_id(self):
        flight = flight_sample()

        url = reverse("airport:flight-detail", args=(flight.id,))

        response = self.client.get(url)
        serializer = FlightDetailSerializer(flight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_forbidden(self):
        airport_1 = airport_sample()
        airport_2 = airport_sample(name="Test Airport")
        route = Route.objects.create(
            source=airport_1,
            destination=airport_2,
        )
        airplane = airplane_sample()
        departure_time = timezone.now()
        arrival_time = departure_time + timedelta(hours=2)
        payload = {
            "route": route,
            "airplane": airplane,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        }
        response = self.client.post(FLIGHTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedCrewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_get_crews(self):
        crew_sample()

        response = self.client.get(CREW_URL)
        crews = Crew.objects.all()
        serializer = CrewListSerializer(crews, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def filter_crews_by_first_name(self):
        crew_1 = crew_sample(first_name="Eliot", last_name="Wang")
        crew_2 = crew_sample(first_name="Kate", last_name="Smith")

        response = self.client.get(
            CREW_URL,
            {"first_name": crew_1.first_name},
        )

        serializer_1 = CrewListSerializer(crew_1)
        serializer_2 = CrewListSerializer(crew_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def filter_crews_by_last_name(self):
        crew_1 = crew_sample(first_name="Eliot", last_name="Wang")
        crew_2 = crew_sample(first_name="Kate", last_name="Smith")

        response = self.client.get(
            CREW_URL,
            {"last_name": crew_1.last_name},
        )

        serializer_1 = CrewListSerializer(crew_1)
        serializer_2 = CrewListSerializer(crew_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_filter_crews_by_roles(self):
        crew_1 = crew_sample(
            first_name="Eliot", last_name="Wang", role=Crew.Roles.CAPTAIN
        )
        crew_2 = crew_sample(
            first_name="Kate", last_name="Smith", role=Crew.Roles.STEWARD
        )

        response = self.client.get(
            CREW_URL,
            {"role": f"{crew_1.role}"},
        )

        serializer_1 = CrewListSerializer(crew_1)
        serializer_2 = CrewListSerializer(crew_2)

        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_retrieve_crews_by_id(self):
        crew = crew_sample()

        url = reverse("airport:crew-detail", args=(crew.id,))

        response = self.client.get(url)
        serializer = CrewSerializer(crew)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "Eliot",
            "last_name": "Wang",
            "role": "CAPTAIN",
        }

        response = self.client.post(CREW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplanesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@test.test",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        test_type = AirplaneType.objects.create(name="Test Type")
        payload = {
            "name": "Airbus",
            "rows": 20,
            "seats_in_row": 5,
            "airplane_type": test_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        airplane = Airplane.objects.get(id=response.data["id"])

        result = {
            "id": airplane.id,
            "name": "Airbus",
            "seats_in_row": 5,
            "rows": 20,
            "airplane_type": test_type,
            "total_number_of_seats": 100,
        }

        for key in result:
            self.assertEqual(result[key], getattr(airplane, key))

    def test_create_airport(self):
        payload = {
            "name": "National Airport",
            "country": "USA",
            "city": "New York",
            "latitude": 51.5007,
            "longitude": 0.1246,
        }
        response = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        airport = Airport.objects.get(id=response.data["id"])

        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))

    def test_create_flight(self):
        airport_1 = airport_sample()
        airport_2 = airport_sample(name="Test Airport")
        route = Route.objects.create(
            source=airport_1,
            destination=airport_2,
        )
        airplane = airplane_sample()
        departure_time = timezone.now()
        arrival_time = departure_time + timedelta(hours=2)
        crew_1 = crew_sample()
        crew_2 = crew_sample(first_name="Zayne", last_name="Koller")
        payload = {
            "route": route.id,
            "airplane": airplane.name,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "crew_1": [crew_1.id, crew_2.id],
        }
        response = self.client.post(FLIGHTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        flight = Flight.objects.get(id=response.data["id"])

        result = {
            "route": route,
            "airplane": airplane,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "crew": flight.crew,
        }

        for key in result:
            self.assertEqual(result[key], getattr(flight, key))

    def test_create_crew(self):
        payload = {
            "first_name": "Eliot",
            "last_name": "Wang",
            "role": "CAPTAIN",
        }
        response = self.client.post(CREW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        crew = Crew.objects.get(id=response.data["id"])

        result = {
            "id": crew.id,
            "first_name": "Eliot",
            "last_name": "Wang",
            "role": "CAPTAIN",
            "full_name": "Eliot Wang",
        }

        for key in result:
            self.assertEqual(result[key], getattr(crew, key))

    def test_create_route(self):
        airport_1 = airport_sample(
            name="National Airport", latitude=51.5007, longitude=0.1246
        )
        airport_2 = airport_sample(
            name="Airport",
            latitude=40.6892,
            longitude=74.0445
        )

        payload = {
            "source": airport_1.name,
            "destination": airport_2.name,
        }

        response = self.client.post(ROUTES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        route = Route.objects.get(id=response.data["id"])

        self.assertEqual(route.distance, 5575)
