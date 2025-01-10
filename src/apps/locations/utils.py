import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache as django_cache
from redis import Redis

User = get_user_model()
logger = logging.getLogger(__name__)


class CacheUtils:
    @staticmethod
    def create_cache_key(user: User) -> str:
        return f"locations:{user.id}"

    @staticmethod
    def get_client() -> Redis:
        """Get redis client"""
        return django_cache._cache.get_client()


cache = CacheUtils.get_client()
