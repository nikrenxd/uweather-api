from rest_framework import serializers

from src.apps.locations.models import Location


class LocationApiDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def to_internal_value(self, data):
        return_data = {
            "name": data["name"],
            "longitude": data["coord"]["lon"],
            "latitude": data["coord"]["lat"],
        }

        return super().to_internal_value(return_data)


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "name",
            "longitude",
            "latitude",
        )

    def create(self, validated_data):
        location, _ = self.Meta.model.objects.get_or_create(**validated_data)
        return location


class LocationListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    current_temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
    min_temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_temperature = serializers.DecimalField(max_digits=5, decimal_places=2)

    def to_internal_value(self, data):
        return_data = {
            "name": data["name"],
            "current_temperature": data["main"]["temp"],
            "min_temperature": data["main"]["temp_min"],
            "max_temperature": data["main"]["temp_max"],
        }

        return super().to_internal_value(return_data)
