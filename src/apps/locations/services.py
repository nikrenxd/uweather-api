import json
import logging

from django.contrib.auth import get_user_model
from httpx import Client
from redis import RedisError

from src.apps.locations.models import Location
from src.apps.locations.utils import CacheUtils, cache
from src.config.base import config

User = get_user_model()
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

    @classmethod
    def get_cache(cls, user: User, page_number: str) -> list[dict] | None:
        cache_key = CacheUtils.create_cache_key(user)

        try:
            data = cache.hget(cache_key, page_number)
            if data:
                data = json.loads(data)
                return data
        except RedisError:
            logger.error("Error when retrieving cached data")

        return None

    @classmethod
    def set_cache(
        cls, user: User, data: list[dict], page_number: str, ttl: int
    ) -> None:
        cache_key = CacheUtils.create_cache_key(user)

        try:
            cache.hset(cache_key, page_number, json.dumps(data))
            cache.expire(cache_key, ttl)
        except RedisError:
            logger.error("Error when updating cached data")

    @classmethod
    def delete_cache_on_change(cls, user: User):
        try:
            cache_key = CacheUtils.create_cache_key(user)
            cache.delete(cache_key)
        except RedisError:
            logger.error("Error on cache invalidation")
