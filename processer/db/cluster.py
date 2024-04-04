from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class Cluster(Model):
    title: str = ''
    member_count: int
    keywords: List[str]
    weight: float
    total_weight: float

    def __init__(self, *args, **kwargs) -> None:

        super(Cluster, self).__init__(entity_options={
            "exclude_from_indexes": ("title", "total_weight", )}, *args, **kwargs)
