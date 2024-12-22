from asyncio import gather
import asyncio
from collections import defaultdict
from os import name

from fastapi import APIRouter

from routing.util.entity2responsetype import entity2responsetype, entity2responsetype_list
from routing.util import chek_notfound
from .router import get_routing_tuple
from .query.speaker import get_speaker, get_speaker_by_name
from .query.speech import get_by_speaker
from .return_models.types.speaker.data import SpeakerSingle, SpeechOverview
router = APIRouter()


@router.get('/data')
async def data(id):
    speaker = await get_speaker.fetch(id)
    chek_notfound.exec(speaker)
    same_name_cor = get_speaker_by_name.fetch(name=speaker['name'])
    speeches_cor = get_by_speaker.fetch(speaker_id=id, limit=None)
    same_name_itr, speeches_itr = await asyncio.gather(same_name_cor, speeches_cor)
    house_to_samename = defaultdict(list)
    for entity in same_name_itr:
        if entity.key.id_or_name == speaker.key.id_or_name:
            continue
        if entity['house'] == '両院':
            house_to_samename['両院総会'].append(
                entity2responsetype(SpeakerSingle, entity))
    speeches = entity2responsetype_list(SpeechOverview, speeches_itr)

    ret = {'speaker': entity2responsetype(
        SpeakerSingle, speaker), 'same_names': list(house_to_samename.items()), 'speeches': speeches}

    return ret


routing_tuple = get_routing_tuple(__file__, router)
