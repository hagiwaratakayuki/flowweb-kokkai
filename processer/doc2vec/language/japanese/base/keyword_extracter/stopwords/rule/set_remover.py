from ja_stopword_remover.remover import Stopword


stopword_set = set()
stopword = Stopword()

stopword_set.update(stopword.demonstrative)
stopword_set.update(stopword.symbol)
stopword_set.update(stopword.verb)
stopword_set.update(stopword.one_character)
stopword_set.update(stopword.postpositional_particle)
stopword_set.update(stopword.slothlib)
stopword_set.update(stopword.auxiliary_verb)
stopword_set.update(stopword.adjective)


def remove_stopwords(words):
    return [word for word in words if word not in stopword_set]


def check_is_stopword(word, *ars, **kwargs):
    return word in stopword_set
