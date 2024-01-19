#!-*- coding:utf-8 -*-


'''
Created on 2015/12/20

@author: Hagiwara Takayuki
'''

import urllib.parse
import re
import unicodedata
from lib.webapi import rest
from typing import Union, Literal, List
import logging
import datetime
import itertools

from typing import Dict, Any
from xml.etree.ElementTree import Element

KUGIRI = re.compile(u'^[\W\s]+$', re.UNICODE + re.MULTILINE)
KANJI_COUNT = u"一二三四五六七八九"
KANJI_COUNT_ONLY = re.compile('^[%s]+$' % KANJI_COUNT)
KANSUUJI_ZERO_TEXT = u'〇0o\W'
KANSUUJI_ZERO_PATTEN = re.compile(
    u'[%s]' % KANSUUJI_ZERO_TEXT, re.IGNORECASE + re.UNICODE)
KANJI_KETA_BASETEXT = u'十百千'
KANJI_KETA_EXTENDTEXT = u'万憶兆京'
KANSUUJI_PATTERN = re.compile(u'([{count}{keta_base}]+[{count}{keta_base}{keta_extend}{zero}]*)[条項節編章節款目](?!委員会)'.format(
    count=KANJI_COUNT, keta_base=KANJI_KETA_BASETEXT, keta_extend=KANJI_KETA_EXTENDTEXT, zero=KANSUUJI_ZERO_TEXT))

KANJI_KETA_MAP = {k: 10 ** v for v, k in enumerate(KANJI_KETA_BASETEXT, 1)}
KANJI_KETA_EXTEND_MAP = {k: 10 ** v for v,
                         k in enumerate(KANJI_KETA_EXTENDTEXT, 4)}

kansuuji = {u'零': '0', u'一': '1', u'壱': '1', u'二': '2', u'弐': '2', u'三': '3',
            u'四': '4', u'五': '5', u'六': '6', u'七': u'7', u'八': '8', u'九': '9'}


lineParserClasses = []


class Speaker:
    def __init__(self, speechRecord: Element, name, speech: str) -> None:
        speech = speechRecord.findtext('speech')
        self.name = name

        self.isWitness = speechRecord.findtext('speakerRole') != None
        self.isUnswornWitness = speechRecord.findtext('speakerRole') == "参考人"
        self.isRequested = self.isUnswornWitness or self.isWitness
        self.isCouncil = re.search(u'^[^\s]+参事\s', speech, re.U) != None
        self.position = speechRecord.findtext('speakerPosition')
        self.group = speechRecord.findtext('speakerGroup')
        self.role = speechRecord.findtext('speakerRole')
        self.isModerater = False
        self.isDietMember = not self.isWitness and not self.isCouncil and self.position == None

    def toDict(self):
        ret = dict(name=self.name)
        if self.position is not None and bool(self.position) == True:
            ret['position'] = self.position
        if self.group is not None and bool(self.group) == True:
            ret['group'] = self.group
        if self.role is not None and bool(self.role) == True:
            ret['role'] = self.role
        if self.isModerater == True:
            ret['isModerater'] = True
        return ret


class SpeechRecord(object):
    order: Any
    speaker: Speaker
    url: str
    isAsModerator: Union[bool, None]
    speech: str
    responseTo: Any

    def __init__(self, speechRecord: Element, order, speaker: Speaker, speech: str):
        self.order = order
        self.speaker = speaker
        self.url = speechRecord.findtext('speechURL')
        self.id = speechRecord.findtext('speechID')
        isAsModerator = False
        headNotes = re.split('\s+', speech, flags=re.U)[0]

        for headNote in re.split('\W', headNotes, re.U):
            striped = headNote.strip()

            if re.search('君$', striped, re.U) is None:

                isAsModerator = '理事' in headNote or re.search(
                    '長$', headNote.strip()) is not None
                if isAsModerator == True:
                    break
        self.isAsModerator = isAsModerator
        self.responseTo = None
        self.speech = re.sub(u'^[^\s]+\s+', u'　', speech, flags=re.U)

    def setResponseTo(self, order):
        self.responseTo = order

    def toDict(self):
        ret = dict(speaker=self.speaker.name,
                   speech=self.speech, url=self.url, id=self.id, order=self.order)
        if self.responseTo != None:
            ret['responseTo'] = self.responseTo
        return ret


class MeetingRecord(object):
    def __init__(self, record: Element):
        self.session = record.findtext('session')
        self.id = record.findtext('issueID')
        self.house = record.findtext('nameOfHouse')
        self.name = record.findtext('nameOfMeeting')
        self.date = record.findtext('date')
        self.issue = record.findtext('issue').replace(u'\D+', u'', re.U)
        self.url = record.findtext('meetingURL')
        self.pdf = record.findtext('pdfURL')
        self.speeches = {}
        self.moderators = []
        year, month, date = [int(token)
                             for token in re.split(u'[^\d]+', self.date)]

        speeches: Dict[Any, SpeechRecord] = {}
        speakers: Dict[str, Speaker] = {}
        prevSpeech = None
        questioner = None
        moderatorSpeech = ""

        for speechRecordNode in record.findall('speechRecord'):
            order = int(speechRecordNode.findtext('speechOrder'))
            speaker = speechRecordNode.findtext('speaker')

            if order == 0:
                self.parseHeaderLog(speechRecordNode, year, month, date)
                continue

            if order == 1:

                self.moderators.append(speaker)
            speech = speechRecordNode.findtext('speech')
            speakerData = speakers.get(speaker) or Speaker(
                speechRecord=speechRecordNode, speech=speech, name=speaker)
            speakers[speaker] = speakerData
            speechRecord = SpeechRecord(
                speechRecordNode, order, speakerData, speech)

            if speechRecord.isAsModerator == False:
                speeches[order] = speechRecord
                speechRecord.setResponseTo(prevSpeech)
                if questioner != speakerData.name and speechRecord.speaker.isDietMember == True:
                    cand = ""

                    for token in speaker:
                        cand += token
                        check = cand + "君"
                        if check in moderatorSpeech:
                            questioner = speakerData
                            prevSpeech = None
                            break

                else:
                    prevSpeech = speechRecord.id

                moderatorSpeech = ""

            else:
                moderatorSpeech += speechRecord.speech
                if speakerData.name not in self.moderators:
                    self.moderators.append(speakerData.name)
                    speakerData.isModerater = True
            endRecord = speechRecord

        hour, minutes = self.getKanjiTime(endRecord.speech, isClose=True)

        self.end = datetime.datetime(
            year, month, date, hour, minutes).isoformat()

        self.speeches = speeches
        self.speakers = speakers

    def toDict(self):
        ret = {}
        for key, prop in self.__dict__.items():
            if key in ['speeches', 'speakers']:
                ret[key] = [obj.toDict() for obj in prop.values()]
            elif hasattr(prop, 'toDict'):
                ret[key] = prop.toDict()
            else:
                ret[key] = prop
        return ret

    def parseHeaderLog(self, speechRecord, year, month, date):

        # sentence = re.sub(u'([^\s]+)\s+([^\s]+)\s*君',u'\\1\\2君',speechRecord.findtext('speech'),re.U)

        sentence = speechRecord.findtext('speech')
        self.headerRecord = sentence
        hour, minutes = self.getKanjiTime(sentence)

        self.start = datetime.datetime(
            year, month, date, hour, minutes).isoformat()

    def getKanjiTime(self, text, isClose=False):
        if text.count(u'正午'):
            return 12, 0

        pt = u'(午前|午後)(.+)時(.+分)?'

        allm = re.findall(pt, text)
        ampm, hour, minute = allm.pop()
        hour = self._parseKanjiNumber(hour)
        if ampm == u'午後':
            hour += 12
        try:

            minute = self._parseKanjiNumber(minute.replace(u'分', '')) or 0
        except Exception:
            print(text)
        return hour, minute

    def _parseKanjiNumber(self, text):
        if not text:
            return

        numText = ''
        match = re.search(u'^.十.$', text)

        if match:
            targets = text.replace(u'十', '')
            for target in targets:
                numString = kansuuji[target]
                numText += numString
            return int(numText)

        match = re.search(u'^.十$', text)
        if match:
            target = text.replace(u'十', '')
            numString = kansuuji[target]
            numText += numString
            numText += '0'
            return int(numText)

        match = re.search(u'^十.$', text)
        if match:
            target = text.replace(u'十', '')
            numText += '1'
            numString = kansuuji[target]
            numText += numString
            return int(numText)
        if text == u'十':
            return 10
        for target in text:

            numString = kansuuji[target]
            numText += numString

        return int(numText)


class MeetingRecords(object):
    total: int
    now: int
    next: Union[Literal[False], int]
    records: List[MeetingRecord]

    def __init__(self, result: Element):

        data = result

        self.total = int(data.findtext('numberOfRecords'))
        self.now = int(data.findtext('startRecord'))
        next = data.findtext('nextRecordPosition')
        if next is not None:
            self.next = int(next)
        else:
            self.next = False

        self.records = []

        for record in data.findall('records/record/recordData/meetingRecord'):

            self.records.append(MeetingRecord(record))


def search(params):

    client = rest.Client('http://kokkai.ndl.go.jp/api/1.0/meeting')
    client.setQueryParamByDict(params)
    status, result = client.send(True)

    if not status:

        logging.error(result)
        return False
    return MeetingRecords(result)
