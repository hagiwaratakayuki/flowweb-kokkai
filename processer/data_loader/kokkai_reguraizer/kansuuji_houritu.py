import re


KANJI_COUNT = r"一二三四五六七八九"
KANJI_COUNT_ONLY = re.compile(r'^[%s]+$' % KANJI_COUNT)
KANSUUJI_ZERO_TEXT = '〇0o\W'
KANSUUJI_ZERO_PATTEN = re.compile(
    '[%s]' % KANSUUJI_ZERO_TEXT, re.IGNORECASE + re.UNICODE)
KANJI_KETA_BASETEXT = '十百千'
KANJI_KETA_EXTENDTEXT = '万憶兆京'
KANSUUJI_PATTERN = re.compile(r'([{count}{keta_base}]+[{count}{keta_base}{keta_extend}{zero}]*)[条項節編章節款目](?!委員会)'.format(
    count=KANJI_COUNT, keta_base=KANJI_KETA_BASETEXT, keta_extend=KANJI_KETA_EXTENDTEXT, zero=KANSUUJI_ZERO_TEXT))

KANJI_KETA_MAP = {k: 10 ** v for v, k in enumerate(KANJI_KETA_BASETEXT, 1)}
KANJI_KETA_EXTEND_MAP = {k: 10 ** v for v,
                         k in enumerate(KANJI_KETA_EXTENDTEXT, 4)}

kansuuji = {'零': '0', '一': '1', '壱': '1', '二': '2', '弐': '2', '三': '3',
            '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}


def convert(speech: str, speechData):
    result = ''
    for sent in speech.split('。'):
        readed = set()

        for target in KANSUUJI_PATTERN.findall(sent):
            if target in readed:
                continue
            readed.add(target)
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
                new = str(value)

            sent = sent.replace(target, new)

        result += sent
        result += '。'

    return result
