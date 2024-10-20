import re
pattern = re.compile(r'^\W+$', re.M)


def convert(text, speecData):
    return pattern.split(text)[0]
