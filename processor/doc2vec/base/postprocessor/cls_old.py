from collections import defaultdict, deque
import keyword
import math
from typing import Dict
import numpy as np

from doc2vec.base.protocol.tokenizer import TokenizerCls
from doc2vec.base.protocol.vectorizer import WordVectorizer

from ..protocol.sentiment import SentimentAnarizer, SentimentVectors, SentimentWeights

from ..protocol.sentiment import SentimentResult
from data_loader.dto import DTO
WORD_2_NORM = {}


def get_norm_weight(filtered_map: Dict[str, Dict]):
    global WORD_2_NORM
    word_2_norm_map = {k: WORD_2_NORM[k]
                       for k in filtered_map.keys() if k in WORD_2_NORM}
    index = 0
    index2word = {}
    norms = []
    for word, value in filtered_map.items():
        if word in WORD_2_NORM:
            continue
        norms.append(value['vector'])
        index2word[index] = word
        index += 1
    if index != 0:

        vectors_array = np.array(norms)
        vectors_norm = np.linalg.norm(vectors_array, axis=1)
        index = 0
        for norm in vectors_norm:
            word = index2word[index]
            word_2_norm_map[word] = norm
            index += 1
            WORD_2_NORM[word] = norm
    index = 0
    index2word = {}
    norms = []
    for word, norm in word_2_norm_map.items():
        norms.append(norm)
        index2word[index] = word
        index += 1
    norms_array = np.array(norms)
    norm_avg = np.average(norms_array)
    weight_array = np.power(norms_array / norm_avg, 2)
    ret = {}
    index = 0
    for weight in weight_array:
        word = index2word[index]
        ret[word] = weight
        index += 1

    return ret


def WeightMap():
    return defaultdict(float)


class postprocesser:
    def __init__(self, tokenaizer: TokenizerCls, sentimentAnalyzer: SentimentAnarizer, vectorizer: WordVectorizer) -> None:
        self._tokenaizer = tokenaizer
        self._sentimentAnalyzer = sentimentAnalyzer

        self._vectoraizer = vectorizer

    def compute(self, args):

        token_lines, vector_map, keyword_set, specifickeywords, data_id = args
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
        word_to_norm_weight = get_norm_weight(filtered_map)
        vector = np.sum([v['vector'] * v['weight'] * word_to_norm_weight[k]
                        for k, v in filtered_map.items()], 0)

        sentimentResults = self._process_senti_total(
            vector_map, vector, sentimentWordMap=sentimentWordMap, sentimentRatio=sentimentRatio)

        scored_keywords = self._extract_keywords(
            filtered_map=filtered_map, vector=vector, keyword_set=keyword_set, specific_keywords=specifickeywords)

        return vector, sentimentResults, scored_keywords, data_id

    def _extract_keywords(self, filtered_map, vector, keyword_set, specific_keywords):
        word_index = dict(enumerate(filtered_map.keys()))

        word_length = len(filtered_map)
        if word_length == 0:
            return []
        try:
            word_vector_array = np.array(
                [filtered_map[word_index[i]]["vector"] for i in range(word_length)])

            norms_from_center = np.linalg.norm(
                word_vector_array - vector, axis=1)
            avg_from_center = np.average(norms_from_center)
            std_from_center = np.std(norms_from_center)
            sorted_array = np.argsort(norms_from_center)
            limit = avg_from_center - std_from_center

            scored_keywords: list[str] = [word_index[i]
                                          for i in sorted_array if norms_from_center[i] <= limit]

            if len(scored_keywords) == 0:
                scored_keywords = [word_index[sorted_array[0]]]

            return [keyword for keyword in scored_keywords if keyword in keyword_set][:5]
        except:
            return []

    def _process_senti_total(self, vector_map, vector, sentimentWordMap, sentimentRatio):
        sentimentVectors = SentimentVectors()

        for sentiment, sentimentWords in sentimentWordMap.items():

            total = sum(sentimentWords.values())

            if total == 0:

                total = 1
            reguraised = {k: v / total for k, v in sentimentWords.items()}

            setattr(sentimentVectors, sentiment, sum(
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
