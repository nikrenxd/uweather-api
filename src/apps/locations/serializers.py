from rest_framework import serializers

from src.apps.locations.models import Location


class CoordinatesSerializer(serializers.Serializer):
    lat = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
    )
    lon = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
    )


class LocationSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    coord = CoordinatesSerializer()

    def to_representation(self, instance):
        new_repr = super().to_representation(instance)

        coords_data = new_repr.pop("coord")
        new_repr["latitude"] = coords_data["lat"]
        new_repr["longitude"] = coords_data["lon"]

        return new_repr


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


class TemperatureSerializer(serializers.Serializer):
    temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    temp_min = serializers.DecimalField(max_digits=5, decimal_places=2)
    temp_max = serializers.DecimalField(max_digits=5, decimal_places=2)


class LocationListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    main = TemperatureSerializer()

    def to_representation(self, instance):
        new_repr = super().to_representation(instance)
        temperature_data = new_repr.pop("main")

        new_repr["current_temperature"] = temperature_data["temp"]
        new_repr["min_temperature"] = temperature_data["temp_min"]
        new_repr["max_temperature"] = temperature_data["temp_max"]

        return new_repr
