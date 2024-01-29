from storage.meeting import Meeting
from itertools import chain
from typing import Any, Dict

from .dto import DTO as Base
import hashlib
from collections import deque
from data_logics import kokkai_meeting, kokkai_speaker, kokkai_speech
from .util import list_runner
from data_loader.kokkai_reguraizer import reguraizers


class DTO(Base):
    meeting_id: str
    house: str


def load(speakerSaver=kokkai_speaker.Saver(), speechSaver=kokkai_speech.Saver(), meetingSaver=kokkai_meeting.Saver()):
    storagemodel = Meeting()
    for session,  meetingChunks in storagemodel.downloadAll():

        speaker_id_map = {}
        speeches = deque()
        meetings = deque()
        yield session, chain.from_iterable((processDownlod(meeting, speakerMap=speaker_id_map, speeches=speeches, meetings=meetings) for meeting in chain.from_iterable(meetingChunks)))
        speakerSaver.save(speaker_id_map=speaker_id_map)
        speechSaver.save(session=session, speeches=speeches)
        meetingSaver.save(meetings=meetings)
    speakerSaver.close()
    meetingSaver.close()
    speechSaver.close()


def processDownlod(meeting: Dict, speakerMap: Dict, speeches: deque, meetings: deque):

    house = meeting['house']

    session = str(meeting['session'])
    _speakerMap = {}
    for speaker in meeting['speakers']:
        name = speaker['name']
        group = speaker.get('group', '')
        position = speaker.get('position', '')
        role = speaker.get('role', '')
        speaker['session'] = session
        speaker['house'] = house
        _speakerMap[name] = {'id': hashlib.md5('_'.join(
            [session, house, name, group, position, role]).encode()).hexdigest(), 'speaker': speaker}
    meeting['moderators'] = {name: _speakerMap[name]
                             for name in meeting['moderators']}
    meetings.append(meeting)
    for speechData in meeting['speeches']:

        speechText = list_runner.run(
            reguraizers, speechData['speech'], speechData)

        dto = DTO()
        dto.title = speechData['speech'][0:20]
        dto.body = speechText
        dto.id = speechData['id']
        dto.author = speechData['speaker']
        dto.author_id = _speakerMap[speechData['speaker']]['id']
        yield dto
        speechData['speaker_id'] = dto.author_id
        speechData['meeting_id'] = meeting["id"]
        speeches.append(speechData)
    for v in _speakerMap.values():
        speakerMap[v['id']] = v['speaker']
