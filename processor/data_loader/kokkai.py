
from collections.abc import Iterable
from operator import itemgetter


from db.memo import Memo

from storage.meeting import Meeting
from itertools import chain
from typing import Dict, Optional, Tuple
import hashlib
import re


from .dto import DTO as Base
from collections import defaultdict, deque
from data_logics import kokkai_meeting, kokkai_speaker, kokkai_speech, kokkai_comittie
from .util import list_runner
from data_loader.kokkai_reguraizer import reguraizers
import unicodedata


number_pt = re.compile(r'\d+')
whitespace_pt = re.compile(r'\s')


class DTO(Base):
    meeting_id: str
    house: str
    keywords: list
    comittie: str
    weight: float
    group: Optional[str]
    session: int
    discussion_id: Optional[str]
    _is_use_title = False


SessionComittieHouseDataType = kokkai_comittie.SessionComittieDataType

MEETING_MAP = {}
MeetingSaver: kokkai_meeting.Saver = None


def SessionComittieHouseData():
    ret: SessionComittieHouseDataType = {}
    ret['max_issue'] = -1
    ret['meetings'] = []
    return ret


def SessionComittieHouseDataMap():
    return defaultdict(SessionComittieHouseData)


def load(storage_model_class=Meeting,
         speaker_saver_class=kokkai_speaker.Saver,
         speech_saver_class=kokkai_speech.Saver,
         meeting_saver_class=kokkai_meeting.Saver,
         comittie_saver_class=kokkai_comittie.Saver,
         session_comittie_saver_class=kokkai_comittie.SessionSaver
         ):
    global MeetingSaver
    storage_model = storage_model_class()
    speech_saver = speech_saver_class()
    speaker_saver = speaker_saver_class()
    MeetingSaver = meeting_saver_class()
    session_comittie_saver = session_comittie_saver_class()
    comittie_saver = comittie_saver_class()
    comittie_map: kokkai_comittie.ComittieMapType = defaultdict(
        kokkai_comittie.ComittieData)
    for session, meetingChunks in storage_model.downloadAll():

        session_comittie_data_map = defaultdict(SessionComittieHouseDataMap)

        speaker_id_map = {}
        speeches = deque()
        meetings = deque()
        comittie_to_speaker = {}
        yield session, chain.from_iterable(processDownlod(comittie_map, session_comittie_data_map, meeting, speaker_id_map=speaker_id_map, speeches=speeches, meetings=meetings, comittie_to_speaker=comittie_to_speaker) for meeting in chain.from_iterable(meetingChunks))
        speaker_saver.save(speaker_id_map=speaker_id_map)
        speech_saver.save(session=session, speeches=speeches)

        session_comittie_saver.save(
            session=session, session_comittie_data_map=session_comittie_data_map)

    session_comittie_saver.close()
    comittie_saver.save(comittie_map=comittie_map)
    comittie_saver.close()

    speaker_saver.close()
    speech_saver.close()


keywordgetter = itemgetter(0)
scoregetter = itemgetter(1)


def processDownlod(comittie_map: kokkai_comittie.ComittieMapType, session_comittie_data_map: Dict[str, Dict[str, SessionComittieHouseDataType]], meeting: Dict, speaker_id_map: Dict, speeches: deque, meetings: deque, comittie_to_speaker: Dict):
    global MEETING_MAP
    MEETING_MAP[meeting['id']] = meeting
    house = meeting['house']
    comittie_name = meeting['name']

    issue = int(number_pt.search(unicodedata.normalize(
        'NFKC', meeting['issue'])).group(0))
    meeting['issue'] = issue
    session_comittie_data = session_comittie_data_map[comittie_name][house]
    if issue > session_comittie_data['max_issue']:
        session_comittie_data['max_issue'] = issue
    session_comittie_data['meetings'].append((house, meeting['id'],))

    comittie_data = comittie_map[comittie_name]
    session = int(meeting['session'])
    str_session = str(session)
    if comittie_data.end < session:
        comittie_data.end = session
    if comittie_data.start > session:
        comittie_data.start = session
    _speaker_name_to_data = {}
    for speaker in meeting['speakers']:
        name = whitespace_pt.sub('', speaker['name'])
        group = speaker.get('group', '')
        position = speaker.get('position', '')
        role = speaker.get('role', '')
        speaker['session'] = session
        speaker['house'] = house
        speaker['comittie'] = comittie_name

        _speaker_name_to_data[name] = {'id': hashlib.md5('_'.join(
            [house, str_session, comittie_name, name, group, position, role]).encode()).hexdigest(), 'speaker': speaker}
    meeting['moderators'] = {name: _speaker_name_to_data[name]
                             for name in meeting['moderators']}
    meetings.append(meeting)

    for speechData in meeting['speeches']:

        striped = speechData['speech'].strip()
        speechText = list_runner.run(
            reguraizers, striped, speechData)

        dto = DTO()
        dto.title = striped[0:20]
        dto.body = speechText
        dto.id = speechData['id']
        dto.author = speechData['speaker']
        dto.author_id = _speaker_name_to_data[speechData['speaker']]['id']
        dto.published = meeting['start']
        dto.house = meeting['house']
        dto.meeting_id = meeting['id']
        dto.comittie = meeting['name']
        dto.group = speechData.get('group')
        dto.discussion_id = speechData.get('discussion_id')
        dto.session = session

        yield dto
        speechData['speaker_id'] = dto.author_id
        speechData['meeting_id'] = meeting["id"]
        speechData['meeting'] = meeting['name']
        speechData['title'] = dto.title
        speechData['house'] = house
        speechData['issue'] = house
        speeches.append(speechData)

    for v in _speaker_name_to_data.values():
        speaker_id_map[v['id']] = v['speaker']


def save_meeting(speech_data_map: Dict[str, Iterable[Tuple[float, list]]]):
    global MEETING_MAP
    for meeting in MEETING_MAP.values():
        MeetingSaver.save(meeting=meeting)
    MEETING_MAP = {}


def close_meeting_saver():
    global MeetingSaver
    MeetingSaver.close()
    MeetingSaver = None
