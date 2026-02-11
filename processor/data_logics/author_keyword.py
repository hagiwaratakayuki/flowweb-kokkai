from pyexpat import model
from typing import DefaultDict, Dict
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.author_keyword import AuthorKeyword


class Saver(ChunkedBatchSaver):
    def __init__(self, size: int = 30, ModelClass=AuthorKeyword):
        self._author_to_keyword: Dict[str,
                                      Dict[str, float]] = DefaultDict(dict)

        self._model_class = ModelClass
        super().__init__(size)

    def put(self, author_id, keywords):
        count = float(len(keywords))
        total_score = (count + 1.0) * count / 2.0
        diff = 0.0
        for k in keywords:
            score = (count - diff) / total_score
            self._author_to_keyword[author_id][k] = self._author_to_keyword[author_id].get(
                k, 0.0) + score

    def close(self, is_return=True):
        for author_id, score_map in self._author_to_keyword.items():
            for keyword, score in score_map.items():
                model = self._model_class()
                model.author_id = author_id
                model.keyword = keyword
                model.score = score
                super().put(model=model)

        return super().close(is_return)
