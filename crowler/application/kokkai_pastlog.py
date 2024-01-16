from storage.meeting import Meeting
from storage.speechlog import SpeechLog
from core.kokkai import pastlog
from core.kokkai import MeetingRecord
from .const import LATEST_SESSION
from storage.meeting import Meeting
from typing import List
import hashlib
from storage.basic import upload_gzip
from db import memo


def crowl(params: dict):
    sessionTo = params.get('sessionTo', LATEST_SESSION)
    startRecord = params.get('startRecord', None)
    crowlResult = pastlog.crowl(startRecord=startRecord, sessionTo=sessionTo)
    if sessionTo not in params:
        value = crowlResult.records[0].id
        memoModel = memo.Model(id='headId')
        memoModel.value = value
        memoModel.upsert()

    upload(session=sessionTo, meetingRecordList=crowlResult.records)

    isEnd = False

    if crowlResult != False:
        if crowlResult.next is False:
            startRecord = None
            if sessionTo == 1:
                isEnd = True
            else:
                sessionTo -= 1
        else:
            startRecord = crowlResult.next

    ret = dict(sessionTo=sessionTo)

    if startRecord is not None:
        ret['startRecord'] = startRecord

    return isEnd, ret


def upload(session: int, meetingRecordList: List[MeetingRecord]):

    meetingRecordDict = {}
    idStringList = []
    for meetingRecord in meetingRecordList:
        meetingRecordDict[meetingRecord.id] = meetingRecord.toDict()
        idStringList.append(meetingRecord.id)
    file = hashlib.md5('+'.join(idStringList).encode()).hexdigest()
    meeting = Meeting()
    meeting.upload(session=session, filename=file, data=meetingRecordDict)
