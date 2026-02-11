import unicodedata


def convert(text: str, speechData):
    return unicodedata.normalize('NFKC', text).upper()
