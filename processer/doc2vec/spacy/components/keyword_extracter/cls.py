from collections import defaultdict
from typing import List
from spacy.tokens import Doc
import numpy as np

from doc2vec.protocol.sentiment import SentimentResult
from data_loader.dto import DTO
from doc2vec.spacy.components.keyword_extracter.protocol import KeywordExtractRule
from doc2vec.util.specified_keyword import SpecifiedKeyword


class BasicKeywordExtratcer:
    def __init__(self, rules: List[KeywordExtractRule], keyword_limit):
        self.rules = rules
        self.keyword_limit = keyword_limit

    def exec(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO):
        results: List[SpecifiedKeyword] = []
        tokenid2keyword = defaultdict(dict)
        for rule in self.rules:
            results, tokenid2keyword = rule.execute(
                doc, vector, sentiment_results, dto, results=results, tokenid2keyword=tokenid2keyword)
        keyword_objects = [
            result for result in results if result.is_force == True]
        index2object = {}
        index = -1
        vectors = []
        for result in results:

            if result.is_force:
                continue
            index += 1
            index2object[index] = result
            vectors.append(result.vector)
        vectors_array = np.array(vectors)
        vectors_array -= vector
        keyword_objects.extend([index2object[index] for index in np.argsort(
            np.absolute(vectors_array).sum(axis=1))[:self.keyword_limit]])
        keywords = sum([['/'.join(tuples) for tuples in keyword_object.to_extender()]
                       for keyword_object in keyword_objects])
        return keywords
