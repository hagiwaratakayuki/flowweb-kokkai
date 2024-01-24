import re
pattern = re.compile('[^\w。、]\w+[^\w。、]', re.M)


def convert(text, speecData):
    return pattern.sub('', text)
