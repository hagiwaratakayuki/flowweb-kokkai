from .regex_pt import regex_pt

stopwords = regex_pt


def check_stopword_with_itr(words):
    return [word for word in words if word not in stopwords]


def check_stopword(word):
    return word not in stopwords
