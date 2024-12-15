from httpx import Client
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from src.apps.locations.models import Location
from src.apps.locations.serializers import LocationSerializer
from src.config.base import config


class LocationViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["GET"], url_path="weather")
    def add_weather(self, request: Request):
        location = request.query_params["location"]

        with Client() as client:
            response = client.get(
                config.EXTERNAL_API_URL,
                params={"q": location, "appid": config.EXTERNAL_API_KEY},
            )

        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()

            serializer = LocationSerializer(data=response_data)
            serializer.is_valid(raise_exception=True)

            Location.objects.create(user=request.user, **serializer.validated_data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
