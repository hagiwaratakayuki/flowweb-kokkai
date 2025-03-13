from doc2vec.spacy.japanese_language.components.keyword_extract.stopwords.list_remover import ichidow
from doc2vec.spacy.japanese_language.components.keyword_extract.stopwords.list_remover import ja_stopword_remover_set
stopword_set = set()
stopword_set.update(ja_stopword_remover_set.stopword_set)
stopword_set.update(ichidow.stopword_set)


def list_remover(words):
    return [word for word in words if word not in stopword_set]
