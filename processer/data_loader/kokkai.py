from numpy import Infinity

from storage.meeting import Meeting
from itertools import chain
from typing import Any, Dict

from .dto import DTO as Base
import hashlib
from collections import defaultdict, deque
from data_logics import kokkai_meeting, kokkai_speaker, kokkai_speech, kokkai_comittie
from .util import list_runner
from data_loader.kokkai_reguraizer import reguraizers


class DTO(Base):
    meeting_id: str
    house: str


def ComittieHouseIssues():
    return defaultdict(list)


def load(storage_model_class=Meeting,
         speaker_saver_class=kokkai_speaker.Saver,
         speech_saver_class=kokkai_speech.Saver,
         meeting_saver_class=kokkai_meeting.Saver,
         comittie_saver_class=kokkai_comittie.Saver,
         session_comittie_saver_class=kokkai_comittie.SessionSaver
         ):
    storage_model = storage_model_class()
    speech_saver = speech_saver_class()
    speaker_saver = speaker_saver_class()
    meeting_saver = meeting_saver_class()
    session_comittie_saver = session_comittie_saver_class()
    comittie_saver = comittie_saver_class()
    comittie_map: kokkai_comittie.ComittieMapType = defaultdict(
        kokkai_comittie.ComittieData)
    for session,  meetingChunks in storage_model.downloadAll():

        session_comittie_data_map = defaultdict(ComittieHouseIssues)

        speaker_id_map = {}
        speeches = deque()
        meetings = deque()
        yield session, chain.from_iterable((processDownlod(comittie_map, session_comittie_data_map, meeting, speaker_id_map=speaker_id_map, speeches=speeches, meetings=meetings) for meeting in chain.from_iterable(meetingChunks)))
        speaker_saver.save(speaker_id_map=speaker_id_map)
        speech_saver.save(session=session, speeches=speeches)
        meeting_saver.save(meetings=meetings)
        session_comittie_saver.save(
            session=session, session_comittie_data_map=session_comittie_data_map)

    session_comittie_saver.close()
    comittie_saver.save(comittie_map=comittie_map)
    comittie_saver.close()

    speaker_saver.close()
    meeting_saver.close()
    speech_saver.close()


def processDownlod(comittie_map: kokkai_comittie.ComittieMapType, session_comittie_data_map: Dict, meeting: Dict, speaker_id_map: Dict, speeches: deque, meetings: deque):

    house = meeting['house']
    comittie_name = meeting['name']
    session_comittie_data_map[comittie_name][house].append(meeting['issue'])
    comittie_data = comittie_map[comittie_name]
    session = int(meeting['session'])
    str_session = str(session)
    if comittie_data.end < session:
        comittie_data.end = session
    if comittie_data.start > session:
        comittie_data.start = session
    _speaker_name_to_data = {}
    for speaker in meeting['speakers']:
        name = speaker['name']
        group = speaker.get('group', '')
        position = speaker.get('position', '')
        role = speaker.get('role', '')
        speaker['session'] = session
        speaker['house'] = house
        _speaker_name_to_data[name] = {'id': hashlib.md5('_'.join(
            [str_session, house, name, group, position, role]).encode()).hexdigest(), 'speaker': speaker}
    meeting['moderators'] = {name: _speaker_name_to_data[name]
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
        dto.author_id = _speaker_name_to_data[speechData['speaker']]['id']
        dto.published = meeting['start']
        yield dto
        speechData['speaker_id'] = dto.author_id
        speechData['meeting_id'] = meeting["id"]
        speeches.append(speechData)
    for v in _speaker_name_to_data.values():
        speaker_id_map[v['id']] = v['speaker']
