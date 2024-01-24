import re
pattern = re.compile('^\W+$', re.M)


def convert(text, speecData):
    return pattern.split(text)[0]
