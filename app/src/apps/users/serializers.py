from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class EmailLoginSerializer(LoginSerializer):
    username = None


class RegisterSerializerBadRequest(serializers.Serializer):
    detail = serializers.CharField(default="Bad request")
