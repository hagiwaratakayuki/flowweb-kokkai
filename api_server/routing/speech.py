import asyncio
from typing import Union
from fastapi import APIRouter, status
from flask import g

from routing.return_models.types.cluster.overview import ClusterOverview
from routing.util.entity2responsetype import entity2responsetype_list
from routing.return_models.types.speech.data import SpeechData

from .query.speech import get_by_discussion_async, get_speech, get_speech_multi
from .query.cluster import get_clusters_by_node
from .return_models.types.speech.single import SpeechS

router = APIRouter()

#response 
@router.get('/data')
async def data(id: Union[int, str]):
    asyncio.sleep(0)
    speech, cluster_datas = await asyncio.gather(get_speech.fetch(id), get_clusters_by_node.fetch(node_id=id))
    cluster_entities, cursor = cluster_datas
    clusters = {'clusters': entity2responsetype_list(
        ClusterOverview, cluster_entities), 'cursor': cursor}
    discussion = None
    if 'discussion_id' in speech:
        discussion = await get_by_discussion_async
    return dict(speech=speech, clusters=clusters, discussion=discussion)
