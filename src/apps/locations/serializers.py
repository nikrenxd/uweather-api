from rest_framework import serializers

from src.apps.locations.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "name",
            "longitude",
            "latitude",
        )

    def to_internal_value(self, data):
        return_data = {
            "name": data["name"],
            "longitude": data["coord"]["lon"],
            "latitude": data["coord"]["lat"],
        }

        return super().to_internal_value(return_data)
