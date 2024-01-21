from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class Cluster(Model):
    title: str = ''
    member_count: int
    short_keywords: List[str]

    def __init__(self, *args, **kwargs) -> None:
        self._entity_options = {"exclude_from_indexes": ("short_keywords", )}
        super(Cluster, self).__init__(*args, **kwargs)
