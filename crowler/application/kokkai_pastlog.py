
from storage.meeting import Meeting
from storage.speechlog import SpeechLog
from core.kokkai import pastlog
from core.kokkai import MeetingRecord
from .const import LATEST_SESSION
from storage.meeting import Meeting
from typing import List
import hashlib
import json
import logging

from db import memo


def resume():
    pagingMemo = memo.Memo.get(id='paging')
    if not pagingMemo:
        logging.error('not crowled')
        return
    params = json.loads(pagingMemo['value'])

    return crowl(params)


def crowl(params: dict):

    sessionTo = params.get('sessionTo', LATEST_SESSION)
    startRecord = params.get('startRecord', None)
    if 'startRecord' not in params:
        print(f'session {sessionTo} crowl start')
    crowlResult = pastlog.crowl(
        startRecord=startRecord, sessionFrom=sessionTo, sessionTo=sessionTo)

    if crowlResult == False:
        startR = startRecord or 1
        print(f'session {sessionTo} start {startR} fail')
        return False

    if 'sessionTo' not in params:
        value = crowlResult.records[0].id
        memoModel = memo.Memo(id='headId')
        memoModel.value = value
        memoModel.upsert()

    upload(session=sessionTo, meetingRecordList=crowlResult.records)

    isEnd = False

    if crowlResult.next is False:
        print(f'crowl end {sessionTo}')
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
    memoModel = memo.Memo(id='paging')
    memoModel.value = json.dumps(ret)
    memoModel.upsert()
    return isEnd, ret


def upload(session: int, meetingRecordList: List[MeetingRecord]):

    meetingRecordDict, idStringList = createDataAndFileName(
        meetingRecordList=meetingRecordList)
    file = hashlib.md5('+'.join(idStringList).encode()).hexdigest()
    meeting = Meeting()
    meeting.upload(session=session, filename=file, data=meetingRecordDict)


def createDataAndFileName(meetingRecordList: List[MeetingRecord]):
    meetingRecords = []
    idStringList = []
    for meetingRecord in meetingRecordList:
        meetingRecords.append(meetingRecord.toDict())
        idStringList.append(meetingRecord.id)
    return meetingRecords, idStringList
