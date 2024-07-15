#!/usr/bin/env python3

"""
This module contains a single function that inserts a new document in a
collection based on the key-value pairs provided.
"""

from pymongo.collection import Collection


def insert_school(mongo_collection, **kwargs):
    """Inserts a new school into the collection and returns the id."""

    if not isinstance(mongo_collection, Collection):
        raise TypeError("mongo_collection must be a collection")

    return mongo_collection.insert_one(kwargs).inserted_id
