#!-*- coding:utf-8 -*-


'''
Created on 2015/12/20

@author: Hagiwara Takayuki
'''
from calendar import monthrange
import json
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


KUGIRI = re.compile(r'^[\W\s]+$', re.UNICODE + re.MULTILINE)
KANJI_COUNT = r"一二三四五六七八九"
KANJI_COUNT_ONLY = re.compile(r'^[%s]+$' % KANJI_COUNT)

KANSUUJI_ZERO_TEXT = r'〇0o零'
KANSUUJI_ZERO_PATTEN = re.compile(
    r'[%s]' % KANSUUJI_ZERO_TEXT, re.IGNORECASE + re.UNICODE)
KANJI_KETA_BASETEXT = r'十百千'
KANJI_KETA_EXTENDTEXT = r'万憶兆京'
KANSUUJI_BASIC = r'[{count}{keta_base}{keta_base}{keta_extend}{zero}]+'.format(
    count=KANJI_COUNT, keta_base=KANJI_KETA_BASETEXT, keta_extend=KANJI_KETA_EXTENDTEXT, zero=KANSUUJI_ZERO_TEXT)
SUUJI_BASIC_PATTERN = re.compile(
    r'\d+|{ksuuji}'.format(ksuuji=KANSUUJI_BASIC))
# KANSUUJI_LOW_PATTERN = re.compile(
#    r'({basic}*)[条項節編章節款目](?!委員会)'.format(basic=KANSUUJI_BASIC))
KANJI_DAY_PATTERN = re.compile(
    r'(昭和|平成|令和)?({basic}|元|\d+)?年?({basic}+|\d+)月({basic}+|\d+)日'.format(basic=KANSUUJI_BASIC))

GENGOU_TO_YEAR = {"昭和": 1926, "平成": 1989, "令和": 2019}
NUMBER_ONLY_PATTERN = re.compile(r'^\d+$')

KANJI_KETA_MAP = {k: 10 ** v for v, k in enumerate(KANJI_KETA_BASETEXT, 1)}
KANJI_KETA_EXTEND_MAP = {k: 10 ** v for v,
                         k in enumerate(KANJI_KETA_EXTENDTEXT, 4)}

NUMBER_ONLY_PATTERN

kansuuji = {r'零': '0', r'一': '1', r'壱': '1', r'二': '2', r'弐': '2', r'三': '3',
            r'四': '4', r'五': '5', r'六': '6', r'七': r'7', r'八': '8', r'九': '9'}


lineParserClasses = []


class Speaker:
    def __init__(self, speechRecord: Element, name, speech: str) -> None:
        speech = speechRecord.findtext('speech')
        self.name = name
        role = speechRecord.findtext('speakerRole')
        self.isWitness = role is not None and role != ""
        self.isUnswornWitness = speechRecord.findtext('speakerRole') == "参考人"
        self.isRequested = self.isUnswornWitness or self.isWitness
        self.isCouncil = re.search(r'^[^\s]+参事\s', speech, re.U) != None
        self.position = speechRecord.findtext('speakerPosition')
        self.group = speechRecord.findtext('speakerGroup')
        self.role = role
        self.isModerater = False
        self.isDietMember = not self.isWitness and not self.isCouncil and (
            self.position is None or self.position == "")

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
        headNotes = re.split(r'\s+', speech, flags=re.U)[0]

        for headNote in re.split(r'\W', headNotes, re.U):
            striped = headNote.strip()

            if re.search('君$', striped, re.U) is None:

                isAsModerator = '理事' in headNote or re.search(
                    '長$', headNote.strip()) is not None
                if isAsModerator == True:
                    break
        self.isAsModerator = isAsModerator
        self.response_to = None
        self.response_from = None
        self.discussion_id = None
        self.speech = re.sub(r'^[^\s]+\s+', r'　', speech, flags=re.U)

    def setResponseTo(self, prevSpeech):
        self.response_to = prevSpeech

    def setResponseFrom(self, nextSpeech):
        self.response_from = nextSpeech

    def setDiscussionId(self, discussionId):
        self.discussion_id = discussionId

    def toDict(self):
        ret = dict(speaker=self.speaker.name,
                   speech=self.speech, url=self.url, id=self.id, order=self.order)
        if self.response_to is not None:
            ret['response_to'] = self.response_to
        if self.response_from is not None:
            ret['response_from'] = self.response_from
        if self.discussion_id is not None:

            ret['discussion_id'] = self.discussion_id
        return ret


class MeetingRecord(object):
    def __init__(self, record: Element):
        global KANJI_DAY_PATTERN
        self.session = record.findtext('session')
        self.id = record.findtext('issueID')
        self.house = record.findtext('nameOfHouse')
        self.name = record.findtext('nameOfMeeting')
        self.date = record.findtext('date')
        self.issue = record.findtext('issue').replace(r'\D+', r'', re.U)
        self.url = record.findtext('meetingURL') or ''
        self.pdf = record.findtext('pdfURL')
        self.speeches = {}
        self.moderators = []

        year, month, date = [int(token)
                             for token in re.split(r'[^\d]+', self.date) if token != '']
        if monthrange(year, month)[1] < date:
            entry = dict(
                severity="MISS_DATE",
                message=' '.join([self.date, self.url])
            )
            print(json.dumps(entry, ensure_ascii=False))
            year = 9999
            month = 1
            date = 1

        speeches: Dict[Any, SpeechRecord] = {}
        speakers: Dict[str, Speaker] = {}
        prevSpeech = None
        questioner = None
        discussion_id = None
        moderatorSpeech = ""
        self.is_freequestion = False
        is_call_witenss = False

        is_explanation = False
        is_explanation_first = False
        explantion_speech = None
        endRecord = None
        for speechRecordNode in record.findall('speechRecord'):
            order = int(speechRecordNode.findtext('speechOrder'))
            speaker = speechRecordNode.findtext('speaker')

            if order == 0:
                self.parseHeaderLog(speechRecordNode, year, month, date)
                continue
            speech = speechRecordNode.findtext('speech')
            if order == 1:
                self.is_freequestion = "自由討議" in speech
                self.moderators.append(speaker)

            speakerData = speakers.get(speaker) or Speaker(
                speechRecord=speechRecordNode, speech=speech, name=speaker)
            speakers[speaker] = speakerData
            speechRecord = SpeechRecord(
                speechRecordNode, order, speakerData, speech)

            if speechRecord.isAsModerator == False:

                speeches[order] = speechRecord

                if questioner != speakerData.name:
                    if is_explanation_first == True:
                        is_explanation_first = False

                    if speechRecord.speaker.isDietMember == True:

                        cand = ""

                        for token in speaker:
                            cand += token
                            checks = [cand + "君", cand + '議員']
                            is_break = False
                            for check in checks:
                                if check in moderatorSpeech:
                                    questioner = speakerData
                                    prevSpeech = None
                                    discussion_id = speechRecord.id
                                    is_break = True
                                    break
                            if is_break:
                                break

                else:
                    prevSpeech = speechRecord
                if prevSpeech is not None:
                    speechRecord.setResponseTo(prevSpeech.id)
                    prevSpeech.setResponseFrom(speechRecord.id)
                if discussion_id is not None:
                    speechRecord.discussion_id = discussion_id

                moderatorSpeech = ""

            else:
                if moderatorSpeech == "":
                    is_explanation = False
                    is_call_witenss = False
                moderatorSpeech += speechRecord.speech
                if speakerData.name not in self.moderators:
                    self.moderators.append(speakerData.name)
                    speakerData.isModerater = True

                if self.is_freequestion is True and speechRecord.speech.count("。") > 1:
                    speeches[order] = speechRecord
                if "趣旨" in moderatorSpeech:
                    is_explanation = True
                    is_explanation_first = True

            endRecord = speechRecord

        if endRecord is not None:
            endyear = year
            endmonth = month
            enddate = date
            hour, minutes = self.getKanjiTime(endRecord.speech)
            if hour == None:
                hour = self._hour
            if minutes == None:
                minutes = self._minutes
            all_m = KANJI_DAY_PATTERN.findall(endRecord.speech)
            is_past = False
            if len(all_m) > 0:
                gengou, kyear, kmonth, kdate = all_m[-1]
                if kyear != '':
                    endyear = self._parseKanjiNumber(kyear) or year
                    if gengou in GENGOU_TO_YEAR:
                        endyear += GENGOU_TO_YEAR[gengou] - 1
                if kmonth != '':

                    endmonth = self._parseKanjiNumber(kmonth)
                    if endmonth == None or endmonth < self._month:
                        endmonth = self._month
                        is_past = True
                if is_past == False:
                    if kdate != '':
                        enddate = self._parseKanjiNumber(kdate) or self._date
            try:
                self.end = datetime.datetime(
                    endyear, endmonth, enddate, hour, minutes).isoformat()
            except:
                entry = dict(
                    severity="TYPO",
                    message=' '.join([endRecord.speech, self.url])
                )
                print(json.dumps(entry, ensure_ascii=False))
                try:
                    self.end = datetime.datetime(
                        self._year, self._month, self._date, hour, minutes).isoformat()
                except:
                    self.end = self.start
        else:
            self.end = self.start

        self.speeches = speeches
        self.speakers = speakers

    def toDict(self):
        ret = {}
        for key, prop in self.__dict__.items():

            if key in ['speeches', 'speakers']:
                ret[key] = [obj.toDict() for obj in prop.values()]
            elif hasattr(prop, 'toDict'):
                ret[key] = prop.toDict()
            elif key.find('_') != 0:
                ret[key] = prop
        return ret

    def parseHeaderLog(self, speechRecord, year, month, date):

        # sentence = re.sub(r'([^\s]+)\s+([^\s]+)\s*君',r'\\1\\2君',speechRecord.findtext('speech'),re.U)

        sentence = speechRecord.findtext('speech')
        self.headerRecord = sentence

        hour, minutes = self.getKanjiTime(sentence)
        if hour == None:
            hour = 10
        if minutes == None:
            minutes = 0

        self.start = datetime.datetime(
            year, month, date, hour, minutes).isoformat()
        self._year = year
        self._month = month
        self._date = date
        self._hour = hour
        self._minutes = minutes

    def getKanjiTime(self, text):

        if text.count(r'正午'):
            return 12, 0

        pt = r'(午前|午後)(.+?)時(.+?分)?(?!現在)'

        allm = re.findall(pt, text)
        if len(allm) == 0:
            return None, None

        ampm, khour, kminute = allm[-1]

        hour = self._parseKanjiNumber(khour)
        is_typo = False
        if hour is not None:
            if ampm == r'午後' and hour != 12:
                hour += 12
            if hour > 23:
                is_typo = True
                hour = 12
        else:
            is_typo = True
        minute = None
        try:

            minute = self._parseKanjiNumber(kminute) or 0
            if minute > 59:
                minute = None
                is_typo = True

        except Exception:
            is_typo = True
        if is_typo == True:
            entry = dict(
                severity="TYPO",
                message=' '.join([text, self.url])
            )
            print(json.dumps(entry, ensure_ascii=False))

        return hour, minute

    def _parseKanjiNumber(self, text):
        text = ''.join(SUUJI_BASIC_PATTERN.findall(text))
        if not text:
            return

        if NUMBER_ONLY_PATTERN.match(text):
            return int(text)
        if text == "零":
            return 0
        numText = ''
        match = re.search(r'^.十.$', text)

        if match:
            targets = text.replace(r'十', '')
            for target in targets:
                numString = kansuuji[target]
                numText += numString
            return int(numText)

        match = re.search(r'^.十$', text)
        if match:
            target = text.replace(r'十', '')
            numString = kansuuji[target]
            numText += numString
            numText += '0'
            return int(numText)

        match = re.search(r'^十.$', text)
        if match:
            target = text.replace(r'十', '')
            numText += '1'
            numString = kansuuji[target]
            numText += numString
            return int(numText)
        if text == r'十':
            return 10
        for target in text:
            if target not in kansuuji:
                continue

            numString = kansuuji[target]
            numText += numString
        if not numText:
            return 0
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
            if not record.findtext('nameOfMeeting') or not record.findtext('date'):
                continue
            self.records.append(MeetingRecord(record))


def search(params):

    client = rest.Client('http://kokkai.ndl.go.jp/api/1.0/meeting')
    client.setQueryParamByDict(params)

    status, result = client.send(True)

    if not status:

        logging.error(result)
        return False

    return MeetingRecords(result)
