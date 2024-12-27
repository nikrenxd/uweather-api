import logging

from httpx import Client

from src.apps.locations.models import Location
from src.config.base import config


logger = logging.getLogger(__name__)


class LocationService:
    @classmethod
    def get_location_data(cls, **kwargs) -> dict | None:
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
            logger.debug("Request failed or got unexpected status code")
            return None

        return response.json()

    @classmethod
    def get_locations_list(cls, locations_data: dict) -> list[dict]:
        """Return list of locations saved in DB"""
        logger.debug("Getting locations list")
        locations = [
            cls.get_location_data(
                lat=location["latitude"],
                lon=location["longitude"],
            )
            for location in locations_data
        ]

        return locations

    @classmethod
    def get_or_create_location(cls, model: type[Location], data: dict) -> Location:
        location = model.objects.get_or_create(**data)[0]
        logger.debug("Returning new or existed location")
        return location
