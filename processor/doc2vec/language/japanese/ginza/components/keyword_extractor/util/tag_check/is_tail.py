from .get_tag import get_tag


def check(token):
    return '接尾辞' in get_tag(token)
