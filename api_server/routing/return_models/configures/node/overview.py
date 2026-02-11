from db.proxy import Node as Base
from typing import Union, Optional
extend_map = {
    'position': Union[str, float]

}
# link_count をフロントでweightとして使用
unpicks = [
    'data',
    'hash',
    'weight',

]
