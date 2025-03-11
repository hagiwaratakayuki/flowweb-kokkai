from .get_tag import get_tag


def check(token):
    return '名詞-普通名詞-一般' == get_tag(token)
