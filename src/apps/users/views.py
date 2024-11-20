from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.users.serializers import RegisterSerializer, RegisterSerializerBadRequest

User = get_user_model()


@extend_schema(tags=["auth"])
class RegisterView(APIView):
    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: None,
            400: RegisterSerializerBadRequest,
        },
    )
    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
