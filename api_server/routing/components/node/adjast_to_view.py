from typing import List, Optional
from data_types.position_data import PositionData

from routing.return_models.types.node.overview import NodeOverview


import numpy as np


import json

# todo ＋－それぞれに中心からの距離の平均を0.5とし　(値　- 平均) /　標準偏差 をゲイン 0.5のシグモイド曲線に代入して最終的な距離を代入


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

        if total_center is None:
            total_center = position
        else:
            total_center += position
        entity_map[index] = {'entity': e,
                             'position': position, 'direction': direction}
        index += 1.0

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
    if isinstance(plus_direction_index.size, int) == True and plus_direction_index.size != 0:

        plus_direction_distances = positions[plus_direction_index]
        plus_direction_distances_std = np.std(plus_direction_distances, axis=0)
        plus_direction_distances_avg = np.average(
            plus_direction_distances, axis=0)
        plus_direction_to_x = (
            plus_direction_distances - plus_direction_distances_avg) / plus_direction_distances_std
        plus_direction_distances = (
            np.tanh((plus_direction_to_x * 2 / 2)) + 1) / 2
        plus_direction_distances[plus_direction_distances > 0.8] = 0.8
        positions[plus_direction_index] = plus_direction_distances
    if isinstance(minus_direction_index.size, int) == True and minus_direction_index.size != 0:

        minus_direction_distances = positions[minus_direction_index]
        minus_direction_distances_std = np.std(
            minus_direction_distances, axis=0)
        minus_direction_distances_avg = np.average(
            minus_direction_distances, axis=0)
        minus_direction_to_x = (
            minus_direction_distances - minus_direction_distances_avg) / minus_direction_distances_std
        minus_direction_distances = (
            np.tanh((minus_direction_to_x * 2 / 2)) + 1) / 2
        minus_direction_distances[minus_direction_distances > 0.8] = 0.8
        positions[minus_direction_index] = minus_direction_distances
    positions *= directions

    ret = [dict(
        id=entity_map[i]['entity'].id or entity_map[i]['entity'].key.name,
        position=positions[i],
        **entity_map[i]['entity']
    )
        for i in range(0, intindex)]
    return ret
