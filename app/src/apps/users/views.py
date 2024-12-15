from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from src.apps.users.serializers import RegisterSerializer

User = get_user_model()


@extend_schema(tags=["auth"])
class RegisterViewSet(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
