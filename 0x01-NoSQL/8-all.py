#!/usr/bin/env python3

"""
This module contains a single function that lists all documents in NoSQL
collection.
"""

from pymongo.collection import Collection


def list_all(mongo_collection):
    """Lists all the documents in a collection."""

    if not isinstance(mongo_collection, Collection):
        raise TypeError("mongo_collection must be a collection")

    if mongo_collection.count_documents({}) == 0:
        return []

    return mongo_collection.find({})
