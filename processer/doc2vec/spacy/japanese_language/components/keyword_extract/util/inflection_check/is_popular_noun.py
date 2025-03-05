from .get_inflection import get_inflection


def check(token):
    return '名詞-普通名詞-一般' == get_inflection(token)
