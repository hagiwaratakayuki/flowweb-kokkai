from doc2vec.indexer.dto import SentimentResult
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
    # type: ignore type length 4
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

    reguraized_center_vecter = sumed_vecter / \
        (np.linalg.norm(sumed_vecter) or 1)  # type: ignore length 4

    vectors4direction = np.zeros(shape=shape)

    vectors4position = np.zeros(shape=shape)

    for index in range(member_count):

        vectors4direction[index] = index2directionvector[index]
        vectors4position[index] = index2sentiments[index].vectors.neutral

    directions = np.dot(vectors4direction, reguraized_center_vecter)

    directions[directions >= 0] = 1
    directions[directions < 0] = -1
    non_regued_distances = np.linalg.norm(
        vectors4position - center_vecter, axis=1)
    max_distance = np.nanmax(non_regued_distances)
    distances = (non_regued_distances / (max_distance or 1)) * directions
    return distances
