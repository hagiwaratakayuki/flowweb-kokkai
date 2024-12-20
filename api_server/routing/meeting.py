from asyncio import gather
from collections import OrderedDict, defaultdict
from application.error_hundling.status_exception import StatusException
from .router import get_routing_tuple

from fastapi import APIRouter, status


from .query.meeting import get_meeting
from .query.speech import get_by_meeting
from .util import chek_notfound
from .util.entity2responsetype import entity2responsetype, entity2responsetype_list
from .return_models.types.speech.overview import SpeechOverview
from .return_models.types.meeting.single import MeetingSingle

router = APIRouter()


@router.get('/data', response_model_exclude_none=True)
async def data(id):
    meeting_cor = get_meeting.fetch(id)
    speech_cor = get_by_meeting.fetch(meeting_id=id)

    meeting_entity, speeches_itr = await gather(meeting_cor, speech_cor)

    chek_notfound.exec(meeting_entity)
    data = entity2responsetype(MeetingSingle, meeting_entity)

    discussion_map = defaultdict(list)
    initial_speaker_map = OrderedDict()
    for speech_entity in speeches_itr:
        discussion_id = speech_entity['discussion_id']
        discussion_map[discussion_id].append(
            entity2responsetype(SpeechOverview, speech_entity))
        if len(discussion_map[discussion_id]) == 1:

            initial_speaker_map[discussion_id] = {
                'name': speech_entity['speaker'], 'id': speech_entity['speaker_id']}
    discussions = [{'speaker': initial_speaker_map[discussion_id],
                    'speeches': discussion_map[discussion_id]}for discussion_id in initial_speaker_map.keys()]
    return dict(data=data, discussions=discussions)


routing_tuple = get_routing_tuple(__file__, router)
