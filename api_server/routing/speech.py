import asyncio

from typing import Union
from fastapi import APIRouter


from .return_models.types.speaker.single import SpeakerSingle

from .return_models.types.speech.overview import SpeechOverview


from .router import get_routing_tuple
from .return_models.types.cluster.overview import ClusterOverview
from .util.entity2responsetype import entity2responsetype, entity2responsetype_list
from .return_models.types.speech.data import SpeechData

from .query.speech import get_by_discussion_async, get_speech
from .query.cluster import get_clusters_by_node
from .query.speaker import get_speaker
from .query.node import get_node
from .return_models.types.speech.single import SpeechSingle

router = APIRouter()

# response


@router.get('/data')
async def data(id: Union[int, str]):
    asyncio.sleep(0)
    speech, cluster_datas, node_entity = await asyncio.gather(get_speech.fetch(id), get_clusters_by_node.fetch(node_id=id), get_node.fetch(id=id))
    speech = entity2responsetype(SpeechSingle, speech)
    cluster_entities, cursor = cluster_datas
    clusters = {'clusters': entity2responsetype_list(
        ClusterOverview, cluster_entities), 'cursor': cursor}
    discussions = None

    speaker_corutine = get_speaker.fetch(speech['speaker_id'])
    if 'discussion_id' in speech:
        discussion_enitties, speake_entity = await asyncio.gather(get_by_discussion_async.fech(speech['discussion_id']), speaker_corutine)
        discussions = entity2responsetype_list(
            SpeechOverview, discussion_enitties)
    else:
        speaker_enity = await speaker_corutine
    speaker = entity2responsetype(SpeakerSingle, speaker_enity)
    return dict(speech=speech, clusters=clusters, discussion=discussions, keywords=node_entity['keywords'], speaker=speaker)


routing_tuple = get_routing_tuple(__file__, router)
