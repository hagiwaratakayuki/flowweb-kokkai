from doc2vec.base.protocol.sentiment import SentimentResult
import numpy as np

# @todo 計算の共通化


def get_position(index2sentiments: dict[int, SentimentResult], cluster_members: frozenset):
    sumed_vecter = None
    is_first = True
    member_count = 0
    index2directionvector = {}

    shape = [0, 0]

    for member in cluster_members:

        sentiment = index2sentiments[member]
        if is_first:
            sumed_vecter = np.zeros(sentiment.vectors.neutral.shape)
            shape[1] = sentiment.vectors.neutral.shape[0]
            is_first = False
        sumed_vecter += sentiment.vectors.neutral
        member_count += 1
    shape[0] = member_count

    center_vecter = sumed_vecter / float(member_count)
    member_count = 0
    for member in cluster_members:

        sentiment = index2sentiments[member]
        vector4direction = sentiment.vectors.positive - sentiment.vectors.negative

        norm = np.linalg.norm(vector4direction)
        if norm == 0:
            vector4direction = sentiment.vectors.neutral - center_vecter
            norm = np.linalg.norm(vector4direction) or 1.0

        index2directionvector[member_count] = vector4direction / norm

        member_count += 1

    reguraized_center_vecter = center_vecter / \
        (np.linalg.norm(center_vecter) or 1)

    vectors4direction = np.zeros(shape=shape)

    vectors4position = np.zeros(shape=shape)

    for index in range(member_count):

        vectors4direction[index] = index2directionvector[index]
        vectors4position[index] = index2sentiments[index].vectors.neutral

    directions: np.ndarray = np.dot(
        vectors4direction, reguraized_center_vecter)
    plus_direction_index = directions >= 0
    minus_direction_index = directions < -1
    directions[plus_direction_index] = 1
    directions[minus_direction_index] = -1

    non_regued_distances = np.linalg.norm(
        vectors4position - center_vecter, axis=1)
    plus_direction_distances = non_regued_distances[plus_direction_index]
    if isinstance(plus_direction_distances.size, int) == True and plus_direction_distances.size == 0:
        plus_max_norm = 1
    else:
        plus_max_norm = np.max(plus_direction_distances) or 1
    minus_direction_distances = non_regued_distances[minus_direction_index]
    if isinstance(minus_direction_distances.size, int) == True and minus_direction_distances.size == 0:
        minus_max_norm = 1
    else:
        minus_max_norm = np.max(minus_direction_distances) or 1

    distances = non_regued_distances * directions
    # 構成要素が一つしかない場合は強制的に0.5、それ以外は最大で0.8
    if isinstance(plus_direction_distances.size, int) == True and plus_direction_distances.size == 1:
        plus_max_norm *= 2
    else:
        plus_max_norm *= 1.25
    if isinstance(minus_direction_distances.size, int) == True and minus_direction_distances.size == 1:
        minus_max_norm *= 2
    else:
        minus_max_norm *= 1.25

    distances[plus_direction_index] /= plus_max_norm
    distances[minus_direction_index] /= minus_max_norm
    return distances
