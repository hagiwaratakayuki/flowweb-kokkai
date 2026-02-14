from .get_tag import get_tag


def check(token):
    return "空白" in get_tag(token)
