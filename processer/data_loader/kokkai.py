from storage.meeting import Meeting
from itertools import chain
from typing import Any, Dict
from .reguraizer import regraizers
from .dto import BaseDataDTO
import hashlib


class DTO(BaseDataDTO):
    def __init__(self, id: Any = '', body: Any = '', author: Any = '', author_id: Any = '', published: Any = None, data: Any = {}, meeting_id: str = ''):
        super().__init__(id, body, author, author_id, published, data)
        self.meeting_id = meeting_id


def load():
    model = Meeting()
    for session,  meetingChunks in model.downloadAll():

        yield session, chain.from_iterable((processDownlod(meeting) for meeting in chain.from_iterable(meetingChunks)))


def processDownlod(meeting: Dict, globalSpeakerMap={}):
    speakerMap = {}
    house = meeting['house']
    session = str(meeting['session'])

    for speaker in meeting['speakers']:
        name = speaker['name']
        group = speaker.get('group', '')
        position = speaker.get('position', '')
        role = speaker.get('role', '')
        speakerMap[name] = {'id': hashlib.md5('_'.join(
            [session, house, name, group, position, role]).encode()).hexdigest(), 'data': speaker}

    for speechData in meeting['speeches']:
        speechText = speechData['speech']
        for reguraizer in reguraizer:
            speechText = reguraizer(speechText)
        dto = BaseDataDTO()
        dto.body = speechText
        dto.id = speechData['id']
        dto.author = speechData['name']
        dto.author_id = speakerMap[speechData['name']]['id']
        yield dto
