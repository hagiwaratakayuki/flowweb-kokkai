
from typing import TypedDict
from google.cloud import datastore


class BaseType(TypedDict):
    @property
    def key(self):
        return datastore.Key()
