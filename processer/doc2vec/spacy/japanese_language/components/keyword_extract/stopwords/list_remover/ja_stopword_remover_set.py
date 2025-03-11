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
