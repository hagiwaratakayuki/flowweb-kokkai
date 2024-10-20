import re
pattern = re.compile(r'[^\w。、]\w+[^\w。、]', re.M)


def convert(text, speecData):
    return pattern.sub('', text)
