import re
import unicodedata

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


def convert(speech):
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
