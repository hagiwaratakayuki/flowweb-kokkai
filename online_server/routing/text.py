from fastapi import APIRouter, status
import json
import numpy as np
import datetime
from .query.text import get_all_summary, get_text_keyword, get_linked_text as linked_text

from .query.cluster import get_clusters_by_text

from routing.return_models.text.overview import TextOverView
from routing.return_models.text.overviews import TextOverViews

from routing.return_models.cluster.overview import ClusterOverView
from routing.return_models.cluster.overviews import ClusterOverViews
from pydantic import BaseModel

from typing import List, Literal
from db.text import Text
from app.error_hundling.status_exception import StatusException
from .router import get_routing_tuple
from data_types.position_data import PositionData


none_type = type(None)
router = APIRouter()


@router.get('/all_summary')
def all_as_vertex() -> list[TextOverView]:
    index = 0.0
    total_center: np.ndarray | None = None
    entity_map = {}
    shape = [0, 0]
    is_first = True
    for e in get_all_summary.fetch():

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

    center: np.ndarray = total_center / index  # type: ignore

    totaldifference = 0.0
    intindex = int(index)
    shape[0] = intindex

    direction_vectors = np.zeros(shape=shape)
    positions_vectors = np.zeros(shape=shape)
    for i in range(0, intindex):

        direction_vectors[i] = entity_map[i]['direction']
        positions_vectors[i] = entity_map[i]['position']
    directions = np.dot(a=direction_vectors, b=center)  # type: ignore
    directions[directions >= 0.0] = 1.0
    directions[directions < 0.0] = -1.0
    positions = np.linalg.norm(positions_vectors, axis=1)
    max_norm = np.max(positions)
    positions *= directions
    positions /= max_norm

    ret = [TextOverView(
        id=entity_map[i]['entity'].id or entity_map[i]['entity'].key.name,
        position=positions[i],
        **entity_map[i]['entity']
    )
        for i in range(0, intindex)]
    return ret


class TextFull(BaseModel):
    title: str = ''
    body: str = ''
    published: datetime.datetime
    author: str = ''
    auther_id: str = ''
    keywords: list[str] = []
    clustres: list[ClusterOverView] | None = None
    clustres_next: None | str = None
    link_to: list[TextOverView] | None = None
    linked_from: list[TextOverView] | None = None
    linked_from_next: Literal[False] | str = False


@router.get('/entity_all', response_model=TextFull, response_model_exclude_none=True)
def get_entity_all(id: int) -> TextFull:
    entity = Text.get(id=id)

    if entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    link_to_ids = [{'id': link_to_id}
                   for link_to_id in entity.get('link_to', [])]
    link_to = [TextOverView(id=e.id or e.key.name, **e)
               for e in Text.get_multi(link_to_ids) or []]  # type: ignore
    keywords = get_text_keyword.fetch(text_id=id)
    """
    cluster_entities, clusters_next = get_clusters_by_text.fetch(text_id=id)

    if cluster_entities == None:
        clusters = None
    else:
        clusters = [ClusterOverView(**e) for e in cluster_entities]
    """
    linked_from_entities, linked_from_next = linked_text.fetch(text_id=id)
    linked_from = [TextOverView(id=e.id or e.key.name, **e)
                   for e in linked_from_entities or []]  # type: ignore

    return TextFull(title=entity["title"],
                    body=entity["body"],
                    published=entity["published"],
                    author=entity["author"],
                    auther_id=entity["author_id"],
                    link_to=link_to,
                    clustres=[],
                    clustres_next="",
                    keywords=keywords,
                    linked_from=linked_from,
                    linked_from_next=linked_from_next
                    )


@router.get('/get_clusters', response_model=ClusterOverViews, response_model_exclude_none=True)
def get_clusters(id: str, cursor: str | None = None) -> ClusterOverViews:
    cluster_entities, next_cursor = get_clusters_by_text.fetch(
        text_id=id, cursor=cursor)

    if cluster_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    clusters = [ClusterOverView(id=e.id, **e)
                for e in cluster_entities]  # type: ignore
    return ClusterOverViews(clusters=clusters, cursor=next_cursor)


@router.get('/get_linked_text', response_model=TextOverViews, response_model_exclude_none=True)
def get_linked_text(id: str, cursor: str) -> TextOverViews:
    text_entities, next_cursor = linked_text.fetch(text_id=id, cursor=cursor)
    if text_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    texts = [TextOverView(id=e.id, **e) for e in text_entities]  # type: ignore
    return TextOverViews(texts=texts, cursor=next_cursor)


@router.get('/get_link_to', response_model=List[TextOverViews], response_model_exclude_none=True)
def get_link_to(ids: list[str]) -> List[TextOverView]:
    text_entities = Text.get_multi(ids)
    if text_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [TextOverView(id=e.id, **e) for e in text_entities]  # type: ignore


routing_tuple = get_routing_tuple(__file__, router)
