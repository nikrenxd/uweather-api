import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def user_credentials():
    return {"email": "user1@mail.com", "password": "1234"}


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "./tests/fixtures/users.json")
        call_command("loaddata", "./tests/fixtures/locations.json")


@pytest.fixture(scope="function")
def user(db):
    return get_user_model().objects.first()


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="function")
def authenticated_client(api_client, user) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client
