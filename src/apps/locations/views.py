from httpx import Client
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.locations.models import Location
from src.apps.locations.serializers import (
    LocationListSerializer,
    LocationCreateSerializer,
    LocationSearchSerializer,
)
from src.config.base import config


class LocationViewSet(GenericViewSet, CreateModelMixin):
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by("name")

    def get_serializer_class(self):
        if self.action == "list":
            return LocationListSerializer
        if self.action == "create":
            return LocationCreateSerializer
        if self.action == "search_locations":
            return LocationSearchSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated = self.paginate_queryset(queryset)

        with Client() as client:
            locations = [
                client.get(
                    config.EXTERNAL_API_URL,
                    params={
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "appid": config.EXTERNAL_API_KEY,
                    },
                ).json()
                for location in paginated
            ]
        serializer = self.get_serializer(data=locations, many=True)
        serializer.is_valid(raise_exception=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="weather")
    def search_locations(self, request: Request):
        location = request.query_params["location"]

        with Client() as client:
            response = client.get(
                config.EXTERNAL_API_URL,
                params={"q": location, "appid": config.EXTERNAL_API_KEY},
            )

        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()
            serializer = self.get_serializer(data=response_data)
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
