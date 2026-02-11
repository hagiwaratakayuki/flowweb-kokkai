from typing import Any
from .model import Model
import datetime
from google.cloud.datastore.key import Key
class Edge(Model):
    linked_from:Any
    link_to:Any
    linked_count:int    
    published:datetime.datetime
    
