from .get_tag import get_tag


def check(token):
    return '接頭' in get_tag(token)
