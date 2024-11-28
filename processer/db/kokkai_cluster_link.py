from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class KokkaiClusterLink(Model):
    from_cluster: str
    to_cluster: str
