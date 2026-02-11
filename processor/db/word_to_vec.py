from .model import Model
import json
import numpy
from google.cloud.datastore import query


class WordToVec(Model):
    vector: str
    word: str

    def __init__(self, word: str, vector: numpy.ndarray) -> None:

        self._entity_options = {"exclude_from_indexes": ("vecter",)}
        self.vector = json.dumps(vector.tolist())
        super(WordToVec, self).__init__(id=word)


def get_vectors(words: str):

    chunked = [words[i:i + 30] for i in range(0, len(words), 30)]
    results = {}
    for chunk in chunked:
        wordtovec_query = WordToVec.query()

        wordtovec_query.add_filter("word", "in", chunk)
        results_chunk = wordtovec_query.fetch()
        for result in results_chunk:
            results[result['word']] = numpy.array(json.loads(result["vector"]))

    return results
