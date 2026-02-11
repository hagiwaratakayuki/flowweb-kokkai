from .model import Model
from google.cloud.datastore.key import Key
from typing import Any, List


class Cluster(Model):
    title: str = ''
    member_count: int
    keywords: List[str]
    weight: float
    total_weight: float
    center: List[Any]

    def __init__(self, *args, **kwargs) -> None:

        super(Cluster, self).__init__(entity_options={
            "exclude_from_indexes": ("title", "total_weight", "center",)}, *args, **kwargs)
