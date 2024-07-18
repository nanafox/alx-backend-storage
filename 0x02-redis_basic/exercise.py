#!/usr/bin/env python3

"""This module contains a class that interacts with the Redis server."""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate the key using the method's qualified name

        # Increment the count for this key
        self._redis.incr(key)

        # Call the original method and return its value
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Implements a cache interface."""

    def __init__(self):
        """Initializes the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the data in the cache and returns the key."""
        key: str = str(uuid4())
        self._redis.set(name=key, value=data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve the value associated with the given key from Redis and
        optionally convert it using a provided callable.

        Args:
            key (str): The key to retrieve the value for.
            fn (Callable, optional): An optional callable to convert the data
                back to the desired format. Defaults to None.

        Returns:
            The retrieved value, optionally converted using `fn`, or
            None if the key does not exist.
        """
        value = self._redis.get(key)

        if value is None:
            return None

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve the value associated with the given key from Redis and
        convert it to a UTF-8 string.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str: The retrieved value as a UTF-8 string, or None if the key
            does not exist.
        """
        return self.get(
            key=key, fn=lambda x: x.decode('utf-8') if x else None
        )

    def get_int(self, key: str) -> int:
        """
        Retrieve the value associated with the given key from Redis and
        convert it to an integer.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            int: The retrieved value as an integer, or None if the key
            does not exist.
        """
        return self.get(key=key, fn=lambda x: int(x) if x else None)
