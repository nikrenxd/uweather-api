import pytest

from src.apps.locations.models import Location
from src.apps.locations.serializers import (
    LocationSearchSerializer,
    LocationSerializer,
    LocationUserDataSerializer,
)
from src.apps.locations.services import LocationService


@pytest.mark.parametrize(
    "city_name, result",
    [
        ("New York", "New York"),
        ("Washington", "Washington"),
        ("California", "California"),
    ],
)
def test_get_location_data(city_name, result):
    location = LocationService.get_location_data(q=city_name)
    serializer = LocationSearchSerializer(location)

    assert location is not None
    assert serializer.data["name"] == result


@pytest.mark.django_db
def test_get_locations_list(user):
    locations = Location.objects.filter(user=user)

    locations_data = LocationSerializer(locations, many=True).data
    locations_raw = LocationService.get_locations_list(locations_data)
    json_result = LocationUserDataSerializer(locations_raw, many=True).data

    assert json_result[0]["name"] == "New York"


test_data = [
    ("New York", 40.714300, -74.006000, "New York"),
    ("California", 38.3004, -76.5074, "California"),
]


@pytest.mark.parametrize("name, lat, lon, result", test_data)
@pytest.mark.django_db
def test_get_or_create_location(user, name, lat, lon, result):
    data = {
        "name": name,
        "latitude": lat,
        "longitude": lon,
        "user": user,
    }
    location = LocationService.get_or_create_location(Location, data)
    assert location.name == result
