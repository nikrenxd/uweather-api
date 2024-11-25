from rest_framework.routers import SimpleRouter

from src.apps.locations.views import LocationViewSet

router = SimpleRouter()

router.register(r"locations", LocationViewSet, basename="locations")
