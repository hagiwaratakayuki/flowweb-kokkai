from datetime import datetime
from typing import Union, List
from util.create_type import create_pydantec_model
from db.proxy import Node

extend_map = {
    'position': {
        'type': Union[str, int],
        'default': None
    }
}
NodeOverView = create_pydantec_model(name_template='NodeOverView', base=Node, unpicks=[
                                     'weight'], extend_map=extend_map)
