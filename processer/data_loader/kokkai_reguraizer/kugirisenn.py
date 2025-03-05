import re
pattern = re.compile(r'^\W+$', re.M)


def convert(text, speechData):
    return pattern.split(text)[0]
