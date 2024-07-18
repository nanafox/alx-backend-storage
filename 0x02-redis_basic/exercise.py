#!/usr/bin/env python3

"""This module contains a class that interacts with the Redis server."""

import redis
from uuid import uuid4
from typing import Union


class Cache:
    """Implements a cache interface."""

    def __init__(self):
        """Initializes the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the data in the cache and returns the key."""
        key: str = str(uuid4())
        self._redis.set(name=key, value=data)
        return key
