from storage.meeting import Meeting
from itertools import chain
from typing import Any, Dict
from .reguraizer import regraizers
from .dto import DTO as Base
import hashlib
from collections import deque
from data_logics import kokkai_meeting, kokkai_speaker, kokkai_speech


class DTO(Base):
    meeting_id: str
    house: str

    def __init__(self, id: Any = '', body: Any = '', author: Any = '', author_id: Any = '', published: Any = None, data: Any = {}):
        super().__init__(id, body, author, author_id, published, data)


def load(speakerSaver=kokkai_speaker.Saver(), speechSaver=kokkai_speech.Saver(), meetingSaver=kokkai_meeting.Saver()):
    storagemodel = Meeting()
    for session,  meetingChunks in storagemodel.downloadAll():
        speaker_id_map = {}
        speeches = deque()
        meetings = deque()
        yield session, chain.from_iterable((processDownlod(meeting, speakerMap=speaker_id_map, speeches=speeches, meetings=meetings) for meeting in chain.from_iterable(meetingChunks)))
        speakerSaver.save(speaker_id_map=speaker_id_map)
        speechSaver.save(speeches=speeches)
        meetingSaver.save(meeting=meetings)
    speakerSaver.close()
    speakerSaver.close()
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
        speechText = speechData['speech']
        for reguraizer in reguraizer:
            speechText = reguraizer(speechText)
        dto = DTO()
        dto.body = speechText
        dto.id = speechData['id']
        dto.author = speechData['name']
        dto.author_id = _speakerMap[speechData['name']]['id']
        yield dto
        speechData['speaker_id'] = dto.author_id
        speeches.append(speechData)
    for v in _speakerMap.values():
        speakerMap[v['id']] = v['speaker']
