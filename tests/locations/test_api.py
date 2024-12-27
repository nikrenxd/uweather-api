import pytest
from django.shortcuts import resolve_url


def test_locations_list(authenticated_client):
    url = resolve_url("locations-list")
    response = authenticated_client.get(url)

    assert response.status_code == 200


def test_locations_search(authenticated_client):
    url = resolve_url("locations-search-locations")
    response = authenticated_client.get(url, query_params={"location": "London"})

    assert response.status_code == 200


def test_locations_create(authenticated_client):
    url = resolve_url("locations-list")
    response = authenticated_client.post(
        url,
        data={
            "name": "California",
            "latitude": 38.3004,
            "longitude": -76.5074,
        },
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_locations_delete(authenticated_client):
    url = resolve_url("locations-detail", pk=1)
    response = authenticated_client.delete(url)

    assert response.status_code == 204
