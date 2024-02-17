from ja_stopword_remover.remover import Stopword


stopword_list = []
stopword = Stopword()

stopword_list.extend(stopword.demonstrative)
stopword_list.extend(stopword.symbol)
stopword_list.extend(stopword.verb)
stopword_list.extend(stopword.one_character)
stopword_list.extend(stopword.postpositional_particle)
stopword_list.extend(stopword.slothlib)
stopword_list.extend(stopword.auxiliary_verb)
stopword_list.extend(stopword.adjective)

stopword_set = set(stopword_list)


def list_remover(words):
    return [word for word in words if word not in stopword_set]
