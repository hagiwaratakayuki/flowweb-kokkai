from ......components.japanese_language.rule import valid_noun_jp


def remover(face):
    return not valid_noun_jp.check_valid_noun(face=face)
