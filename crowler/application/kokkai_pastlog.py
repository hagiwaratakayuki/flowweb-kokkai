from storage.meeting import Meeting
from storage.speechlog import SpeechLog
from core.kokkai import pastlog
from core.kokkai import MeetingRecord
from .const import HOUSES
from storage.meeting import Meeting
from typing import List
import hashlib
from storage.basic import upload_gzip


def crowl(params):

    return {}


def upload(session: int, meetingRecordList: List[MeetingRecord]):

    meetingRecordDict = {}
    idStringList = []
    for meetingRecord in meetingRecordList:
        meetingRecordDict[meetingRecord.id] = meetingRecord.toDict()
        idStringList.append(meetingRecord.id)
