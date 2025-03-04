from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)

from airport.serializers import (
    AirplaneListSerializer,
    AirportListSerializer,
    CrewListSerializer,
    FlightListSerializer,
)

airplane_get_parameters = [
    OpenApiParameter(
        name="name",
        type=OpenApiTypes.STR,
        description="Search airplanes by name (case insensitive).",
        examples=[
            OpenApiExample(
                name="Boeing Example",
                value="Boeing",
                summary="Filter airplanes containing 'Boeing' in the name.",
            ),
        ],
    ),
    OpenApiParameter(
        name="seats_in_row",
        type=OpenApiTypes.INT,
        description="Search airplanes by number of seats per row.",
        examples=[
            OpenApiExample(
                name="9 seats example",
                value=9,
                summary="Filter airplanes with 9 seats per row.",
            ),
        ],
    ),
    OpenApiParameter(
        name="rows",
        type=OpenApiTypes.INT,
        description="Search airplanes by number of rows.",
        examples=[
            OpenApiExample(
                name="30 rows example",
                value=30,
                summary="Filter airplanes with 30 rows.",
            ),
        ],
    ),
    OpenApiParameter(
        name="airplane_type",
        type=OpenApiTypes.STR,
        description="Search airplanes by type.",
        examples=[
            OpenApiExample(
                name="Narrow-body example",
                value="Narrow-body",
                summary="Filter airplanes with 'Narrow-body' type.",
            ),
        ],
    ),
]

airplane_get_responses = {
    200: OpenApiResponse(
        response=AirplaneListSerializer,
        description="A list of airplanes matching the given filters.",
        examples=[
            OpenApiExample(
                "Filter by name example response",
                value=[
                    {
                        "id": 6,
                        "name": "Boeing 787 Dreamliner",
                        "airplane_type": "Wide-body",
                        "total_number_of_seats": 360,
                    },
                    {
                        "id": 2,
                        "name": "Boeing Business Jet",
                        "airplane_type": "Business",
                        "total_number_of_seats": 16,
                    },
                ],
            ),
            OpenApiExample(
                "Filter by number of seats in rows example response",
                value=[
                    {
                        "id": 6,
                        "name": "Boeing 787 Dreamliner",
                        "airplane_type": "Wide-body",
                        "total_number_of_seats": 360,
                    }
                ],
            ),
            OpenApiExample(
                "Filter by number of rows example response",
                value=[
                    {
                        "id": 5,
                        "name": "Airbus A319",
                        "airplane_type": "Narrow-body",
                        "total_number_of_seats": 180,
                    }
                ],
            ),
            OpenApiExample(
                "Filter by type example response",
                value=[
                    {
                        "id": 5,
                        "name": "Airbus A319",
                        "airplane_type": "Narrow-body",
                        "total_number_of_seats": 180,
                    },
                    {
                        "id": 4,
                        "name": "Airbus A320",
                        "airplane_type": "Narrow-body",
                        "total_number_of_seats": 210,
                    },
                ],
            ),
        ],
    )
}

airport_get_parameters = [
    OpenApiParameter(
        name="name",
        type=OpenApiTypes.STR,
        description="Search airplanes by name.",
        examples=[
            OpenApiExample(
                name="Search airport with name Lviv",
                value="Lviv",
                summary="Search airport with name Lviv.",
            )
        ],
    ),
    OpenApiParameter(
        name="city",
        type=OpenApiTypes.STR,
        description="Search airplanes by name.",
        examples=[
            OpenApiExample(
                name="Search airport in city Lviv",
                value="Lviv",
                summary="Search airport in city Lviv.",
            )
        ],
    ),
    OpenApiParameter(
        name="country",
        type=OpenApiTypes.STR,
        description="Search airplanes by country.",
        examples=[
            OpenApiExample(
                name="Search airport in country Ukraine",
                value="Ukraine",
                summary="Search airport in country Ukraine.",
            )
        ],
    ),
]

airport_get_responses = {
    200: OpenApiResponse(
        response=AirportListSerializer,
        description="A list of airports matching the given filters.",
        examples=[
            OpenApiExample(
                "Filter by name example response",
                value={
                    "id": 14,
                    "name": "Lviv Danylo Halytskyi Intl",
                    "city": "Lviv",
                    "country": "Ukraine",
                },
            ),
            OpenApiExample(
                "Filter by city example response",
                value={
                    "id": 14,
                    "name": "Lviv Danylo Halytskyi Intl",
                    "city": "Lviv",
                    "country": "Ukraine",
                },
            ),
            OpenApiExample(
                "Filter by country example response",
                value=[
                    {
                        "id": 1,
                        "name": "Boryspil Airport",
                        "city": "Kyiv",
                        "country": "Ukraine",
                    },
                    {
                        "id": 14,
                        "name": "Lviv Danylo Halytskyi Intl",
                        "city": "Lviv",
                        "country": "Ukraine",
                    },
                ],
            ),
        ],
    )
}

crew_get_parameters = [
    OpenApiParameter(
        name="first_name",
        type=OpenApiTypes.STR,
        description="Search crew by first name.",
        examples=[
            OpenApiExample(
                name="Search crew by first name Caleb",
                value="Caleb",
                summary="Search crew by first name Caleb.",
            )
        ],
    ),
    OpenApiParameter(
        name="last_name",
        type=OpenApiTypes.STR,
        description="Search crew by last name.",
        examples=[
            OpenApiExample(
                name="Search crew by last name Adams",
                value="Adams",
                summary="Search crew by last name Adams.",
            )
        ],
    ),
    OpenApiParameter(
        name="role",
        type=OpenApiTypes.STR,
        description="Search crew by role.",
        examples=[
            OpenApiExample(
                name="Search crew by role CAPTAIN",
                value="CAPTAIN",
                summary="Search crew by role CAPTAIN.",
            )
        ],
    ),
]

crew_get_responses = {
    200: OpenApiResponse(
        response=CrewListSerializer,
        description="A list of crews matching the given filters.",
        examples=[
            OpenApiExample(
                "Filter by first name example response",
                value=[
                    {
                        "id": 1,
                        "full_name": "Caleb Adams",
                        "role": "Pilot in Command"
                    }
                ],
            ),
            OpenApiExample(
                "Filter by last name example response",
                value=[
                    {
                        "id": 1,
                        "full_name": "Caleb Adams",
                        "role": "Pilot in Command"
                    }
                ],
            ),
            OpenApiExample(
                "Filter by role example response",
                value=[
                    {
                        "id": 1,
                        "full_name": "Caleb Adams",
                        "role": "Pilot in Command"
                    },
                    {
                        "id": 10,
                        "full_name": "James Walker",
                        "role": "Pilot in Command"
                    },
                    {
                        "id": 16,
                        "full_name": "Kate Smith",
                        "role": "Pilot in Command"
                    },
                ],
            ),
        ],
    )
}

flight_get_parameters = [
    OpenApiParameter(
        name="routes",
        type=OpenApiTypes.INT,
        description="Search flight by routes.",
        examples=[
            OpenApiExample(
                name="Search flight by route 1",
                value=1,
                summary="Flight by route 1.",
            )
        ],
    ),
    OpenApiParameter(
        name="airplanes",
        type=OpenApiTypes.STR,
        description="Search flight by airplanes.",
        examples=[
            OpenApiExample(
                name="Search flight by airplane ATR 72",
                value="ATR 72",
                summary="Flight by airplane ATR 72.",
            )
        ],
    ),
]

flight_get_responses = {
    200: OpenApiResponse(
        response=FlightListSerializer,
        description="A list of flights matching the given filters.",
        examples=[
            OpenApiExample(
                "Filter by route example response",
                value=[
                    {
                        "id": 1,
                        "route": "Kyiv (Ukraine) -> Lviv (Ukraine)",
                        "airplane": "Airbus A319",
                        "departure_time": "2025-03-06T21:00:00+02:00",
                        "arrival_time": "2025-03-06T23:00:00+02:00",
                        "crew": [
                            {
                                "id": 1,
                                "full_name": "Caleb Adams",
                                "role": "Pilot in Command",
                            },
                            {
                                "id": 2,
                                "full_name": "Michael Johnson",
                                "role": "Flight Attendant",
                            },
                            {
                                "id": 13,
                                "full_name": "Zayne Roberts",
                                "role": "Other staff",
                            },
                            {
                                "id": 14,
                                "full_name": "Lucas White",
                                "role": "Co-Pilot"
                            },
                        ],
                    }
                ],
            ),
            OpenApiExample(
                "Filter by airplanes example response",
                value=[
                    {
                        "id": 1,
                        "route": "Kyiv (Ukraine) -> Lviv (Ukraine)",
                        "airplane": "Airbus A319",
                        "departure_time": "2025-03-06T21:00:00+02:00",
                        "arrival_time": "2025-03-06T23:00:00+02:00",
                        "crew": [
                            {
                                "id": 1,
                                "full_name": "Caleb Adams",
                                "role": "Pilot in Command",
                            },
                            {
                                "id": 2,
                                "full_name": "Michael Johnson",
                                "role": "Flight Attendant",
                            },
                            {
                                "id": 13,
                                "full_name": "Zayne Roberts",
                                "role": "Other staff",
                            },
                            {
                                "id": 14,
                                "full_name": "Lucas White",
                                "role": "Co-Pilot"
                            },
                        ],
                    }
                ],
            ),
        ],
    )
}
