import math


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    latitude_1 = math.radians(lat1)
    latitude_2 = math.radians(lat2)

    longitude_1 = math.radians(lon1)
    longitude_2 = math.radians(lon2)

    distance_between_latitudes = latitude_2 - latitude_1
    distance_between_longitudes = longitude_2 - longitude_1

    a = math.sin(distance_between_latitudes / 2) ** 2 + math.sin(
        distance_between_longitudes / 2
    ) ** 2 * math.cos(latitude_1) * math.cos(latitude_2)

    c = 2 * math.asin(math.sqrt(a))

    return round(earth_radius * c)
