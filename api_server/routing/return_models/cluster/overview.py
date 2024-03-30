from pydantic import BaseModel
from typing import Union
from db.proxy import Cluster
from util.create_type import create_type
ClusterOverView = create_type(name_template='ClusterOverView', base=Cluster)
