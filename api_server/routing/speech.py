import asyncio
from typing import Union
from fastapi import APIRouter

from .return_models.types.speech.overview import SpeechOverview


from .router import get_routing_tuple
from .return_models.types.cluster.overview import ClusterOverview
from .util.entity2responsetype import entity2responsetype, entity2responsetype_list
from .return_models.types.speech.data import SpeechData

from .query.speech import get_by_discussion_async, get_speech
from .query.cluster import get_clusters_by_node
from .return_models.types.speech.single import SpeechSingle

router = APIRouter()

# response


@router.get('/data')
async def data(id: Union[int, str]):
    asyncio.sleep(0)
    speech, cluster_datas = await asyncio.gather(get_speech.fetch(id), get_clusters_by_node.fetch(node_id=id))
    speech = entity2responsetype(SpeechSingle, speech)
    cluster_entities, cursor = cluster_datas
    clusters = {'clusters': entity2responsetype_list(
        ClusterOverview, cluster_entities), 'cursor': cursor}
    discussion = None
    if 'discussion_id' in speech:
        discussion = await get_by_discussion_async(speech['discussion_id'])
        discussion = entity2responsetype(SpeechOverview, speech)

    return dict(speech=speech, clusters=clusters, discussion=discussion)


routing_tuple = get_routing_tuple(__file__, router)
