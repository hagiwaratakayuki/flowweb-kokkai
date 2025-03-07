from collections import defaultdict
from typing import Callable, Dict, List
from spacy.tokens import Doc
import numpy as np

from doc2vec.protocol.sentiment import SentimentResult
from data_loader.dto import DTO
from doc2vec.spacy.components.keyword_extracter.protocol import KeywordExtractRule, ExtractResultDTO
from doc2vec.util.specified_keyword import SpecifiedKeyword


class BasicKeywordExtratcer:
    def __init__(self, rules: List[KeywordExtractRule], keyword_limit=5):
        self.rules = rules
        self.keyword_limit = keyword_limit

    def initialize(self, projeccter: Callable):
        self.projecter = projeccter

    def exec(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO):

        results = ExtractResultDTO()
        for rule in self.rules:
            results = rule.execute(
                doc=doc,
                vector=vector,
                sentiment_results=sentiment_results,
                dto=dto,
                results=results,
                projecter=self.projecter
            )

        if len(results.keywords) == 0:
            return []
        result_keywords = results.get_keywords()
        keyword_objects = [
            result for result in result_keywords if result.is_force == True]

        index2object = {}
        index = -1
        vectors = []
        for result_keywords in result_keywords:

            if result_keywords.is_force:
                continue
            index += 1
            index2object[index] = result_keywords
            vectors.append(result_keywords.vector)

        vectors_array = np.array(vectors)
        vectors_array -= vector

        distances = np.absolute(vectors_array).sum(axis=1)
        avg_distace = np.average(distances)

        count = 0
        for index in np.argsort(distances):

            if count >= self.keyword_limit or distances[index] > avg_distace:
                break

            count += 1
            keyword_objects.append(index2object[index])

        keywords = sum([['/'.join(tuples) for tuples in keyword_object.to_extender()]
                       for keyword_object in keyword_objects], [])
        return keywords
