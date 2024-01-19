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
from storage.basic import upload_gzip
from db import memo


def crowl(params: dict):
    sessionTo = params.get('sessionTo', LATEST_SESSION)
    startRecord = params.get('startRecord', None)
    if 'startRecord' not in params:
        logging.info(f'session {sessionTo} crowl start')
    crowlResult = pastlog.crowl(startRecord=startRecord, sessionTo=sessionTo)
    memoModel = memo.Model(id='paging')
    memoModel.value = json.dumps(
        {'sessionTo': sessionTo, 'startRecord': startRecord})
    memoModel.upsert()
    if crowlResult == False:
        startR = startRecord or 1
        logging.error(f'session {sessionTo} start {startR} fail')
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
                logging.info(f'crowl end {sessionTo}')
                sessionTo -= 1
        else:
            startRecord = crowlResult.next
    else:
        return False

    ret = dict(sessionTo=sessionTo)

    if startRecord is not None:
        ret['startRecord'] = startRecord

    return isEnd, ret


def upload(session: int, meetingRecordList: List[MeetingRecord]):

    meetingRecordDict, idStringList = createDataAndFileName(
        meetingRecordList=meetingRecordList)
    file = hashlib.md5('+'.join(idStringList).encode()).hexdigest()
    meeting = Meeting()
    meeting.upload(session=session, filename=file, data=meetingRecordDict)


def createDataAndFileName(meetingRecordList: List[MeetingRecord]):
    meetingRecordDict = {}
    idStringList = []
    for meetingRecord in meetingRecordList:
        meetingRecordDict[meetingRecord.id] = meetingRecord.toDict()
        idStringList.append(meetingRecord.id)
    return meetingRecordDict, idStringList
