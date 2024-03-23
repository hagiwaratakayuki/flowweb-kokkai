from datetime import datetime
from typing import Union, List
from util.create_types import create_pydantec_model
from db.proxy import Node

extend_map = {
    'position': {
        'type': Union[str, int],
        'default': None
    }
}
NodeOverView = create_pydantec_model(name='NodeOverView', base=Node, unpicks=[
                                     'weights'], extend_map=extend_map)
