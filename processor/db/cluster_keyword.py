from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class ClusterKeyword(Model):
    cluster_id: str
    keyword: str
