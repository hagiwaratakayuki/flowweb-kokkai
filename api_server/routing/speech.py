import asyncio

from typing import Union
from fastapi import APIRouter

from .return_models.types.node.overview import NodeOverview


from .return_models.types.speaker.single import SpeakerSingle

from .return_models.types.speech.overview import SpeechOverview


from .router import get_routing_tuple
from .return_models.types.cluster.overview import ClusterOverview
from .util.entity2responsetype import entity2responsetype, entity2responsetype_list
from .return_models.types.speech.data import SpeechData

from .query.speech import get_by_discussion_async, get_speech
from .query.cluster import get_clusters_by_node
from .query.speaker import get_speaker
from .query.node import get_link_from_node, get_node, get_link_to_node
from .return_models.types.speech.single import SpeechSingle

router = APIRouter()

# response


@router.get('/data')
async def data(id: Union[int, str]):
    await asyncio.sleep(0)
    speech_entity, cluster_datas, node_entity = await asyncio.gather(get_speech.fetch(id), get_clusters_by_node.fetch(node_id=id), get_node.fetch(id=id))

    speech = entity2responsetype(SpeechSingle, speech_entity)
    cluster_entities, cursor = cluster_datas
    clusters = {'overviews': entity2responsetype_list(
        ClusterOverview, cluster_entities), 'cursor': cursor}
    discussions = None

    speaker_corutine = get_speaker.fetch(speech_entity['speaker_id'])
    link_from_corutine = get_link_from_node.fetch(
        node_id=node_entity.key.id_or_name)
    link_to_corutine = get_link_to_node.fetch(node=node_entity)
    if 'discussion_id' in speech:
        discussion_enitties, speaker_entity, link_from_fetchresults, link_to_entities = await asyncio.gather(get_by_discussion_async.fech(speech['discussion_id']), speaker_corutine, link_from_corutine, link_to_corutine)
        discussions = entity2responsetype_list(
            SpeechOverview, discussion_enitties)
    else:

        speaker_entity, link_from_fetchresults, link_to_entities = await asyncio.gather(speaker_corutine, link_from_corutine, link_to_corutine)
    speaker = entity2responsetype(SpeakerSingle, speaker_entity)
    link_to = entity2responsetype_list(NodeOverview, link_to_entities)
    link_from_itr, link_from_cursor = link_from_fetchresults
    link_from_responses = entity2responsetype_list(NodeOverview, link_from_itr)
    link_from = {'nodes': link_from_responses, 'cursor': cursor}
    return dict(speech=speech, clusters=clusters, discussion=discussions, keywords=node_entity['keywords'], speaker=speaker, link_from=link_from, link_to=link_to)


routing_tuple = get_routing_tuple(__file__, router)
