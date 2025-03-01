from .get_inflection import get_inflection


def check(token):
    return '接尾辞' in get_inflection(token)
