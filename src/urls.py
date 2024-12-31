from dj_rest_auth import views
from dj_rest_auth.jwt_auth import get_refresh_view
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework import routers

from src.apps.locations.views import LocationViewSet
from src.apps.users.views import RegisterViewSet

router = routers.DefaultRouter()

router.register(r"api/auth/register", RegisterViewSet, basename="register")
router.register(r"api/locations", LocationViewSet, basename="locations")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # Authentication
    path("api/auth/login", views.LoginView.as_view(), name="login"),
    path("api/auth/refresh", get_refresh_view().as_view(), name="token_refresh"),
    path("api/auth/logout", views.LogoutView.as_view(), name="logout"),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
