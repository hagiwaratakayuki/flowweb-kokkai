from .get_tag import get_tag


def check(token):
    tag = get_tag(token)
    return '接尾辞' in tag and '形状詞的' in tag
