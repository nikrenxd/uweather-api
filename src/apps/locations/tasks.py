from celery import shared_task
from celery.result import AsyncResult

from src.apps.locations.services import LocationService


@shared_task
def task_get_location(location_name: str) -> AsyncResult:
    location_data = LocationService.get_location_data(q=location_name)
    return location_data


@shared_task
def task_get_user_locations(locations: list[dict]) -> AsyncResult:
    locations = LocationService.get_locations_list(locations)
    return locations
