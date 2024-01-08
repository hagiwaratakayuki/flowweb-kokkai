#!-*- coding:utf-8 -*-


'''
Created on 2015/12/20

@author: Hagiwara Takayuki
'''

import urllib.parse
import re
import unicodedata
from lib.webapi import rest


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


def classBuilder(cls, *args, **kwargs):
    def ret():
        return cls(*args, **kwargs)


lineParserClasses = []


class MeetingRecords(object):
    def __init__(self, result: Element):

        data = result

        self.total = int(data.findtext('numberOfRecords'))
        self.now = int(data.findtext('startRecord'))
        self.next = int(data.findtext('nextRecordPosition') or False)
        self.records = []

        for record in data.findall('records/record/recordData/meetingRecord'):

            self.records.append(MeetingRecord(record))


class MeetingRecord(object):
    def __init__(self, record: Element):
        self.session = record.findtext('session')
        self.house = record.findtext('nameOfHouse')
        self.name = record.findtext('nameOfMeeting')
        self.date = record.findtext('date')
        self.issue = record.findtext('issue').replace(u'号', u'')
        self.url = record.findtext('meetingURL')
        self.pdf = record.findtext('pdfURL')
        self.discussionChunks = []
        year, month, date = [int(token)
                             for token in re.split(u'[^\d]+', self.date)]
        maxorder = -1

        speeches: Dict[Any, SpeechRecord] = {}
        ord_chunks = []
        startOrder = 1
        is_foreword = True

        for speechRecord in record.findall('speechRecord'):
            order = int(speechRecord.findtext('speechOrder'))

            if order == 0:
                self.parseHeaderLog(speechRecord, year, month, date)
                continue

            if order == 1:
                moderator = record.speaker
                self.moderator = moderator
            else:
                is_foreword = record.speaker != moderator
            record = SpeechRecord(speechRecord, order)
            speeches[order] = record
            if order > maxorder:
                maxorder = order
                endRecord = record

            if KUGIRI.search(record.speech.splitlines().pop()):

                ord_chunks.append((startOrder, order))
                startOrder = order + 1
            elif KUGIRI.search(record.speech):
                if record.speaker == self.moderator:

                    ord_chunks.append((startOrder, order - 1,))
                    startOrder = order
                else:
                    ord_chunks.append((startOrder, order))
                    startOrder = order + 1
        if startOrder < maxorder:
            ord_chunks.append((startOrder, maxorder,))
        hour, minutes = self.getKanjiTime(endRecord.speech, isClose=True)

        self.end = datetime.datetime(year, month, date, hour, minutes)

        self.speeches = speeches

        isGist = False

        gistStart = None
        gistEnd = None
        questionStart = None
        discussionChunks = []
        discussionChunk = None
        checkTexts = []
        for startOrder, endOrder in ord_chunks:

            isDiscussion = False
            isFirst = True
            for order in range(startOrder, min(endOrder, maxorder) + 1):
                record = speeches[order]

                if record.speaker != self.moderator:
                    checkTexts = []

                    if isFirst and not record.isLeader:
                        isFirst = False

                        if record.isRequested:

                            if isGist:
                                self._setCampaign(
                                    speeches, discussionChunks, gistEnd, gistStart)

                            isGist = True

                            gistStart = order
                            gistEnd = endOrder

                else:
                    checkTexts.append(record.speech)

                    if order < maxorder and speeches[order + 1].speaker == self.moderator:

                        continue
                    checkText = u'\n'.join(checkTexts)

                    flag = u"趣旨" in checkText and order < maxorder

                    if flag:

                        if isGist:
                            self._setCampaign(
                                speeches, discussionChunks, gistEnd, gistStart)

                        isGist = True
                        gistStart = order+1
                        gistEnd = endOrder
                        continue

                    isDiscussion = re.search(
                        u'質疑|質問|討議|討論|尋問|審議|論議|論弁|論辯|論判|附議|訊問|審尋|鞫問|借問', checkText)

                    if isDiscussion:
                        if order < maxorder and speeches[order + 1].isRequested:
                            if isGist:
                                self._setCampaign(
                                    speeches, discussionChunks, gistEnd, gistStart)

                            isGist = True

                            gistStart = order
                            gistEnd = endOrder
                            isFirst = False
                            continue
                        questionStart = order + 1

                        if questionStart == endOrder:
                            break

                        discussionChunk = DiscussionChunk(
                            questionStart, gistStart)
                        discussionChunk.parse(
                            endOrder, speeches, self.moderator)
                        discussionChunks.append(discussionChunk)

                        isGist = False
                        gistStart = None
                        gistEnd = None
                        break

        if isGist:

            # 趣旨弁明と演説のみの場合
            self._setCampaign(speeches, discussionChunks, maxorder, gistStart)

        self.discussionChunks = discussionChunks

    def _setCampaign(self, speeches, discussionChunks, maxorder, gistStart):
        discussions = DiscussionChunk(maxorder, gistStart)
        discussions.setGist(speeches, self.moderator)
        campaigns = {}

        ignores = discussions.gistMap.copy()
        ignores[self.moderator] = True
        for order in range(gistStart, maxorder + 1):
            speech = speeches[order]
            if speech.speaker in ignores:
                continue
            campaigns.setdefault(speech.speaker, []).append(speech)
        discussions.campaigns = campaigns
        discussionChunks.append(discussions)

    def _setParticipantsInit(self, name):
        name = re.sub(u'\s+', u'', name, flags=re.U)

        self.participants[name] = {'speech': False,
                                   'discussion': {}, 'speechOrder': []}

    def parseHeaderLog(self, speechRecord, year, month, date):

        self.participants = {}
        # sentence = re.sub(u'([^\s]+)\s+([^\s]+)\s*君',u'\\1\\2君',speechRecord.findtext('speech'),re.U)

        sentence = speechRecord.findtext('speech')
        self.headerRecord = sentence
        hour, minutes = self.getKanjiTime(sentence)

        self.start = datetime.datetime(year, month, date, hour, minutes)

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


class Speaker:
    pass


class SpeechRecord(object):
    def __init__(self, speechRecord: Element, order):
        self.speakerPosition = False
        self.isAdministrator = False
        self.order = order
        self.speaker = speechRecord.findtext('speaker')
        speech = speechRecord.findtext('speech')

        self.isWitness = re.search(u'^[^\s]+証人\s', speech, re.U) != None
        self.isUnswornWitness = re.search(
            u'^[^\s]+参考人\s', speech, re.U) != None
        self.isRequested = self.isUnswornWitness or self.isWitness
        self.isCouncil = re.search(u'^[^\s]+参事\s', speech, re.U) != None
        self.isLeader = re.search(u'^[^\s]+[^房]長\s', speech, re.U) != None

        self.speech = re.sub(u'^[^\s]+\s+', u'　', speech, flags=re.U)
        if not self.isRequested:
            self._setAdministratorPosition(speech)

    def _normalizeSpeech(self, speech):
        speech = unicodedata.normalize("NFKC", speech)
        speech = speech.upper()

        readed = {}
        for target in KANSUUJI_PATTERN.findall(speech):
            if target in readed:
                continue
            readed[target] = True
            new = ''
            if KANJI_COUNT_ONLY.search(target):
                for token in target:
                    new += kansuuji[token]
            else:
                value = 0
                keta = 1
                extend_keta = 1

                tal = list(target)
                tal.reverse()
                lastten = False

                lastbbasekata = 0
                for token in tal:
                    if lastten:
                        nowten = token in KANJI_KETA_MAP
                        if nowten or token in KANJI_KETA_EXTEND_MAP:
                            value += lastbbasekata * extend_keta
                        lastten = nowten

                    if KANSUUJI_ZERO_PATTEN.match(token):

                        keta *= 10
                        continue

                    else:
                        lastten = token in KANJI_KETA_MAP

                    if lastten:
                        keta = extend_keta * KANJI_KETA_MAP[token]
                        lastbbasekata = KANJI_KETA_MAP[token]
                        continue
                    if token in KANJI_KETA_EXTEND_MAP:
                        keta = extend_keta = KANJI_KETA_EXTEND_MAP[token]
                        continue

                    value += int(kansuuji[token]) * keta
                    keta *= 10
                if lastten:
                    value += extend_keta * KANJI_KETA_MAP[token]
                new = value
            speech = speech.replace(target, new)

        return speech

    def _setAdministratorPosition(self, speech):
        match = re.search(u"(^[^\s]+)\(([^)]+)\)\s", speech, re.U)

        if match:
            speakerPosition = u""
            if re.search(u'君$', match.group(1)):
                speakerPosition = re.sub(
                    u'^\W+', u'', match.group(1), flags=re.U)
            elif len(match.group(2)) > 1:
                speakerPosition = match.group(2)
            self.isAdministrator = any(
                [position in speakerPosition for position in [u"大臣", u'内閣官房長官', u'大臣補佐官']])
            if self.isAdministrator:
                self.speakerPosition = speakerPosition
        else:
            match = re.search(u'^[^\s]+', speech, re.U)
            if not match:
                return
            target = re.sub(u'\W', u'', match.group(0), flags=re.UNICODE)

            self.isAdministrator = any(
                [position in target for position in [u"大臣", u'内閣官房長官', u'大臣補佐官']])
            if self.isAdministrator:

                speakerPosition = ([position for position in [
                                   u'内閣官房長官', u'大臣補佐官'] if position in target] or [False])[0]
                if not speakerPosition:
                    name = u""
                    for word in self.speaker:
                        name += word
                        if not name in target:
                            old = re.sub(u'.$', u'', name)
                            speakerPosition = target.replace(old, u'')
                self.speakerPosition = speakerPosition

    def _checkIsEnd(self, speech):
        line = []
        isEnd = False
        for line in "".splitlines():
            if re.search('^[\W\s]+$', line, re.U):
                break
        text = u'\n'.join(line)
        chunks = [chunk for chunk in re.findall(
            u"[^。]+。", text, re.U) if not re.search(u"^\W", chunk, re.U)]
        if chunks:
            tail = chunks[0]
            isEnd = any([test in tail for test in [u'以上です', u'終']])
        self.isEnd = isEnd

    def toDict(self):
        ret = dict(speaker=self.speaker, speech=self.speech)
        return ret


class DiscussionChunk(object):
    """
    pairs of question answer
    """

    def __init__(self, questionStart=None, gistStart=None):
        self.questionStart = questionStart
        self.gistStart = gistStart

        self.gistMap = {}
        self.questioners = []
        self.discussions = []
        self.campaigns = {}

    def parse(self, questionEnd, speeches, moderator):

        self.questionEnd = questionEnd
        self.setGist(speeches, moderator)
        self.setQuestion(speeches, moderator)

    def bindGist(self):
        if not self.gistMap or not self.discussions:
            return
        if self.gistMap:

            for discussion in self.discussions:

                for gister, gist in self.gistMap.items():
                    if gister in discussion.atendees or gister in discussion.getIndexText():

                        discussion.gist.append(gist)

    def setGist(self, speeches, moderator):
        if self.gistStart == None:

            return

        gistMap = {}
        for order in range(self.gistStart, self.questionStart):
            speech = speeches[order]
            if speech.speaker == moderator or speech.isLeader or speech.isCouncil:
                continue
            gistMap.setdefault(speech.speaker, []).append(speech)
        self.gistMap = dict([(gister, Gist(gister, gist),)
                            for gister, gist in gistMap.items()])

        self.bindGist()

    def setQuestion(self, speeches, moderator):
        questioner = None
        lastQuestionOrders = {}

        if self.questionStart is None and self.questionEnd is None:
            return
        maxorder = self.questionEnd

        for order in range(self.questionStart, maxorder + 1):
            record = speeches[order]

            if record.speaker != moderator and not record.isLeader and not record.isCouncil and not record.isRequested:

                lastQuestionOrders[record.speaker] = order
                if not questioner:
                    questioner = record.speaker
                    discussionStart = order
        speakerMap = {}

        while questioner and discussionStart < maxorder:

            discussion = []

            lastQuestionOrder = lastQuestionOrders[questioner]

            for order in range(discussionStart, lastQuestionOrder+1):

                record = speeches[order]

                speakerMap[record.speaker] = True
                if record.speaker != moderator:
                    discussion.append(record)

            questioner = None
            continueFlag = False

            for order in range(lastQuestionOrder + 1, maxorder):
                record = speeches[order]
                notSpeached = not speakerMap.has_key(record.speaker)
                notModerater = record.speaker != moderator
                notIsRequested = not record.isRequested
                notIsAdministrator = not record.isAdministrator

                if notSpeached and notModerater and notIsRequested and notIsAdministrator:
                    self.discussions.append(
                        Discussion(discussionStart, discussion))
                    questioner = record.speaker
                    discussionStart = order
                    continueFlag = True
                    break

                if record.speaker != moderator:
                    discussion.append(record)
            if continueFlag:
                continue
            self.discussions.append(Discussion(discussionStart, discussion))

        self.bindGist()


class Discussion(object):
    docId = None

    def __init__(self, start, speeches):
        self.start = start
        self.speeches = speeches
        self.questioner = speeches[0].speaker
        self.atendees = set([speech.speaker for speech in speeches])
        self.gist = []
        self.administrators = []

    def getIndexText(self):
        return u'\n\n'.join([record.speech for record in self.speeches])


class Gist(object):
    docId = None

    def __init__(self, gister, gist):
        self.gist = gist
        self.gister = gister
        self.start = self.gist[0].order
        self.discussions = []

    def addDiscussions(self, discussion):
        self.discussions.append(discussion)

    def getText(self):
        return u'\n'.join([record.speech for record in self.gist])


class Campaign(object):
    def __init__(self, speaker, gist, speech):
        self.speech = speech
        self.gist = gist
        self.speaker = speaker


def createUrl(params):
    query = urllib.parse.quote(
        '&'.join([key + '=' + value for key, value in params.items()])
    )
    url = 'http://kokkai.ndl.go.jp/api/1.0/meeting?' + query
    return url


def search(params):

    client = rest.Client('http://kokkai.ndl.go.jp/api/1.0/meeting')
    client.setQueryParamByDict(params)
    status, result = client.send(True)

    if not status:

        print(result)
        return False
    return MeetingRecords(result)
