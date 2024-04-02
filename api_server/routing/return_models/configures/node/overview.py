from db.proxy import Node as Base
from typing import Union, Optional
extend_map = {
    'position': Union[str, int]

}
unpicks = [
    'weight',
    'hash',
    'linked_count'
]
