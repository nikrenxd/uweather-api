from django.db.models import QuerySet
from httpx import Client

from src.apps.locations.models import Location
from src.config.base import config


class LocationService:
    @classmethod
    def get_location_data(cls, **kwargs) -> dict:
        """Takes request parameters and return response from api call"""

        default_params = {"appid": config.EXTERNAL_API_KEY}
        with Client(params=default_params) as client:
            response = client.get(
                config.EXTERNAL_API_URL,
                params={
                    **kwargs,
                },
            )

        if response.status_code != 200:
            return None

        return response.json()

    @classmethod
    def get_locations_list(cls, paginated_locations: QuerySet) -> list[dict]:
        return [
            cls.get_location_data(
                lat=location.latitude,
                lon=location.longitude,
            )
            for location in paginated_locations
        ]

    @classmethod
    def get_or_create_location(cls, model: type[Location], data: dict) -> Location:
        location = model.objects.get_or_create(**data)[0]
        return location
