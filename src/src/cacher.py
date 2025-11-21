# src/cacher.py

from django.core.cache import cache
from django.forms.models import model_to_dict


def get_cached_object(cache_key):
    """
    Try to get data from cache.
    """
    return cache.get(cache_key)


def set_cached_object(cache_key, obj, timeout=None):
    """
    Store object in cache after serializing it.
    """
    data = model_to_dict(obj)
    cache.set(cache_key, data, timeout)
    return data


def get_or_set_cache(cache_key, queryset_func, timeout=None):
    """
    Generic function to:
    - Get from cache
    - If not found, query DB
    - Serialize and cache
    """

    data = cache.get(cache_key)

    if data is not None:
        return data

    obj = queryset_func()

    if obj is None:
        return None

    data = model_to_dict(obj)
    cache.set(cache_key, data, timeout)

    return data
