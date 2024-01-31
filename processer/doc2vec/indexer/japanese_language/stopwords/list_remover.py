from ja_stopword_remover.remover import StopwordRemover
REMOVER_OBJ = StopwordRemover()


def list_remover(words):
    return REMOVER_OBJ.remove([words])[0]
