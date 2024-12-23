from django.core.cache import cache
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.locations.models import Location
from src.apps.locations.serializers import (
    LocationCreateSerializer,
    LocationSearchSerializer,
    LocationSerializer,
    LocationUserDataSerializer,
)
from src.apps.locations.tasks import task_get_location, task_get_user_locations


class LocationViewSet(GenericViewSet, CreateModelMixin):
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by("name")

    def get_serializer_class(self):
        if self.action == "list":
            return LocationSerializer
        if self.action == "create":
            return LocationCreateSerializer
        if self.action == "search_locations":
            return LocationSearchSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        cache.delete(self.request.user.id)
        serializer.save(user=self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        paginated_data = self.paginate_queryset(queryset)

        location_serializer = self.get_serializer(paginated_data, many=True)
        data = location_serializer.data

        locations = task_get_user_locations.delay(data).get(timeout=1)

        serializer = LocationUserDataSerializer(data=locations, many=True)
        serializer.is_valid(raise_exception=True)

        response_data = serializer.data
        return self.get_paginated_response(response_data)

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
