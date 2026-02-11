

from .get_tag import get_tag


def check(token):
    return "助数詞" in get_tag(token)
