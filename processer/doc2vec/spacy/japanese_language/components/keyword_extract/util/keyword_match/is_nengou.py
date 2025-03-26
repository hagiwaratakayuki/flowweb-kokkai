

from doc2vec.spacy.util.keywords_match import keywords_match


年号 = {'明治', '大正', '昭和', '平成', '令和'}


def 年号であるか否か(token, is_negative_match=False):
    return keywords_match(token=token, keywords=年号, is_nagative_match=is_negative_match)
