from collections import defaultdict, deque
import math
import numpy as np

from .dto import SentimentWeights, SentimentVector, SentimentResult
from data_loader.dto import DTO


def WeightMap():
    return defaultdict(float)


class Indexer:
    def __init__(self, tokenaizer, sentimentAnalyzer, is_use_title) -> None:
        self._tokenaizer = tokenaizer
        self._sentimentAnalyzer = sentimentAnalyzer
        self._is_use_title = is_use_title

    def parse(self, dto: DTO):

        if self._is_use_title == True:
            text = dto.title + '\n' + dto.body
        else:
            text = dto.body

        token_lines, specifickeywords = self._tokenaizer.exec(text, dto)

        token_map = {}
        for verbs, line in token_lines:
            for verb in verbs:
                token_map[verb] = True

        return token_lines, list(token_map.keys()), specifickeywords, dto.id

    def compute(self, args):

        token_lines, vector_map, specifickeywords, data_id = args
        nodes = []
        count = 0
        for subnodes, line in token_lines:

            subcount = len(subnodes)

            sublen = subcount - int(subcount > 1)
            scored_subnodes = [(face, 1 - math.sin(math.pi * float(position) / float(sublen)) * 0.8 -
                                0.1 * float(position) / float(sublen),) for position, face in enumerate(subnodes)]
            nodes.append((scored_subnodes, count, line, ))
            count += 1
        if count == 0:

            return None, None, None, data_id
        nodeslen = count - int(count > 1)
        key_map = defaultdict(float)
        sentimentWordMap = defaultdict(WeightMap)
        sentimentRatio = defaultdict(float)
        for subnodes, position, line in nodes:

            weights, positionWeight = self._computeWait(
                subnodes, position, nodeslen)
            self._processSentiment(line, weights, positionWeight,
                                   sentimentRatio=sentimentRatio, sentimentWordMap=sentimentWordMap)

            for k, v in weights.items():
                key_map[k] += v

        total = sum(key_map.values())
        reguraised = {k: v / total for k, v in key_map.items()}

        filtered_map = {k: {'vector': vector_map[k], 'weight': w} for k, w in reguraised.items(
        ) if vector_map.get(k, False) is not False}

        vector = np.sum([v['vector'] * v['weight']
                        for k, v in filtered_map.items()], 0)

        sentimentResults = self._process_senti_total(
            vector_map, vector, sentimentWordMap=sentimentWordMap, sentimentRatio=sentimentRatio)

        scored_keywords = self._extract_keywords(
            filtered_map=filtered_map, vector=vector, specific_keywords=specifickeywords)

        return vector, sentimentResults, scored_keywords, data_id

    def _extract_keywords(self, filtered_map, vector, specific_keywords):
        word_index = dict(enumerate(filtered_map.keys()))

        word_length = len(filtered_map)
        if word_length == 0:
            return []
        norms = np.linalg.norm(
            np.array([filtered_map[word_index[i]]["vector"] for i in range(word_length)]) - vector, axis=1)
        avg = np.average(norms)
        std = np.std(norms)
        sorted_array = np.argsort(norms)
        limit = avg - std

        scored_keywords: list[str] = [word_index[i]
                                      for i in sorted_array if norms[i] <= limit][:5]
        if len(scored_keywords) == 0:
            scored_keywords = [word_index[sorted_array[0]]]

        return scored_keywords

    def _process_senti_total(self, vector_map, vector, sentimentWordMap, sentimentRatio):
        sentimentVectors = SentimentVector()

        for sentiment, sentimentWords in sentimentWordMap.items():

            total = sum(sentimentWords.values())

            if total == 0:

                total = 1
            reguraised = {k: v / total for k, v in sentimentWords.items()}
            setattr(sentimentVectors, sentiment,  sum(
                [vector_map[k] * w for k, w in reguraised.items() if vector_map.get(k, False) is not False]))

        total = sum(sentimentRatio.values())
        sentimentWeights = SentimentWeights()
        for sentiment, weight in sentimentRatio.items():
            setattr(sentimentWeights, sentiment, weight / total)
        ret = SentimentResult()
        ret.vectors = sentimentVectors
        ret.weights = sentimentWeights

        return ret

    def _processSentiment(self, line: str, weigts: defaultdict, positionWeight: float, sentimentWordMap: dict, sentimentRatio: dict):
        sentiments = self._analizeSentiment(line)

        for face, weight in weigts.items():
            for sentiment, sWeight in sentiments.items():
                sentimentWordMap[sentiment][face] += weight * \
                    sWeight * positionWeight
        for sentiment, sWeight in sentiments.items():
            sentimentRatio[sentiment] += sWeight * positionWeight

    def _analizeSentiment(self, line):
        return self._sentimentAnalyzer.exec(line)

    def _computeWait(self, subnodes, position, nodeslen):
        weights = defaultdict(float)
        nodeWeight = 1 - math.sin(math.pi * position /
                                  nodeslen) * 0.6 - 0.1 * position / nodeslen
        for surface, subscore in subnodes:
            weights[surface] += subscore * nodeWeight
        return weights, nodeWeight
