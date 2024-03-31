from pydantic import BaseModel
from typing import Union
from db.proxy import Cluster
from util.create_type import create_type
ClusterOverview = create_type(name_template='ClusterOverview', base=Cluster)
