from typing import List, Optional
from data_types.position_data import PositionData
from routing.node import none_type
from routing.return_models.types.node.overview import NodeOverview


import numpy as np


import json


def adjast_to_view(itr) -> List[NodeOverview]:
    index = 0.0
    total_center: Optional[np.ndarray] = None
    entity_map = {}
    shape = [0, 0]
    is_first = True

    for e in itr:

        data: PositionData = json.loads(e['data'])['sentiment']

        position = np.array(data['position'])

        direction = np.array(data['direction'])
        if is_first == True:
            is_first = False
            shape[1] = direction.shape[0]

        if type(total_center) == none_type:
            total_center = position
        else:
            total_center += position
        entity_map[index] = {'entity': e,
                             'position': position, 'direction': direction}
        index += 1.0

    totaldifference = 0.0
    intindex = int(index)
    shape[0] = intindex

    direction_vectors = np.zeros(shape=shape)
    positions_vectors = np.zeros(shape=shape)

    for i in range(0, intindex):

        direction_vectors[i] = entity_map[i]['direction']
        positions_vectors[i] = entity_map[i]['position']
    directions = np.dot(a=direction_vectors, b=total_center)  # type: ignore

    plus_direction_index = directions >= 0.0
    minus_direction_index = directions < 0.0
    directions[plus_direction_index] = 1.0
    directions[minus_direction_index] = -1.0
    positions = np.linalg.norm(positions_vectors, axis=1)

    plus_max_norm = np.max(positions[plus_direction_index]) or 1
    minus_max_norm = np.max(positions[minus_direction_index]) or 1
    if plus_direction_index.size[0] == 1:
        plus_max_norm *= 2
    if minus_direction_index.size[0] == 1:
        minus_max_norm *= 2

    positions *= directions
    positions[plus_direction_index] /= plus_max_norm
    positions[minus_direction_index] /= minus_max_norm
    ret = [NodeOverview(
        id=entity_map[i]['entity'].id or entity_map[i]['entity'].key.name,
        position=positions[i],
        **entity_map[i]['entity']
    )
        for i in range(0, intindex)]
    return ret
