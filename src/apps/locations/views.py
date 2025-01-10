import logging

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from src.apps.locations.models import Location
from src.apps.locations.serializers import (
    LocationCreateSerializer,
    LocationSearchSerializer,
    LocationSerializer,
    LocationUserDataSerializer,
)
from src.apps.locations.services import LocationService
from src.apps.locations.tasks import task_get_location, task_get_user_locations

logger = logging.getLogger(__name__)


class LocationViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by("name")

    def get_serializer_class(self) -> Serializer:
        if self.action == "create":
            return LocationCreateSerializer
        if self.action == "search_locations":
            return LocationSearchSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.debug("perform_create deleting cache")
        LocationService.delete_cache_on_change(self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug("perform_destroy deleting cache")
        LocationService.delete_cache_on_change(self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        page_number = request.query_params.get("page", 1)
        user = request.user

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        location_serializer = self.get_serializer(page, many=True)
        data = location_serializer.data

        locations = LocationService.get_cache(user, page_number)
        if not locations:
            locations = task_get_user_locations.delay(data).get(timeout=5)
            LocationService.set_cache(user, locations, page_number, 180)

        serializer = LocationUserDataSerializer(data=locations, many=True)
        serializer.is_valid(raise_exception=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Cookie"))
    @action(detail=False, methods=["GET"], url_path="weather")
    def search_locations(self, request: Request) -> Response:
        location = request.query_params["location"]

        response_data = task_get_location.delay(location).get(timeout=1)

        if not response_data:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
