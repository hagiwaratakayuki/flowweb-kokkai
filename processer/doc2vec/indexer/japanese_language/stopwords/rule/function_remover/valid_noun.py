from doc2vec.components.japanese_language.rule import valid_noun_jp


def valid_noun(face):
    return not valid_noun_jp.check_valid_noun(face=face)
