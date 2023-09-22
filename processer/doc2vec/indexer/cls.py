from collections import defaultdict
import math
import numpy as np
from .dto import SentimentWeights,SentinmentVector, SentimentResult


def WeightMap():
    return defaultdict(float)

class Indexer:
    def __init__(self, tokenaizer, vectaizer, sentimentAnalyzer) -> None:
        self._tokenaizer = tokenaizer
        self._vectaizer = vectaizer
        self._sentimentAnalyzer = sentimentAnalyzer
       
        
    def exec(self, text:str):
        
        nodes = []
        count = 0
        key_map = defaultdict(float)
        sentimentWordMap = defaultdict(WeightMap) 
        sentimentRatio = defaultdict(float)


        for subnodes, line in self._tokenaizer.exec(text):
            
            subcount = len(subnodes)

            
            sublen = subcount - int(subcount > 1 )       
            scored_subnodes = [ (face, 1 - math.sin(math.pi * float(position) / float(sublen) ) * 0.8  - 0.1 * float(position) / float(sublen),) for position, face in enumerate(subnodes)]
            nodes.append((scored_subnodes, count, line, ))
            count += 1
        if count == 0:
            return None, None
        nodeslen  = count - int(count > 1)
    
       
        for subnodes, position, line in nodes:
           
            
            weights, positionWeight = self._computeWait(subnodes, position, nodeslen)
            self._processSentiment(line, weights, positionWeight, sentimentRatio=sentimentRatio, sentimentWordMap=sentimentWordMap)
        
            for k, v in weights.items():
                key_map[k] += v


        
        total = sum(key_map.values())
        reguraised = {k:v / total for k, v in key_map.items()}
        vector_map:dict[str, np.ndarray] =  self._vectaizer.exec_dict(key_map.keys())
        filtered_map = {k:{'vector':vector_map[k], 'weight':w } for k, w in  reguraised.items() if isinstance(vector_map[k], bool) == False}
       
        vector = np.sum([v['vector'] * v['weight'] for k, v in  filtered_map.items()],0)
      
        sentimentResults = self._process_senti_total(vector_map, vector, sentimentWordMap=sentimentWordMap, sentimentRatio=sentimentRatio)
        word_index = list(filtered_map.keys())
    
        norms = np.linalg.norm(np.array([v['vector']  for v in  filtered_map.values()]) - vector, axis=1)
        avg = np.average(norms)
        #std = np.std(norms)
        sorted_array = np.argsort(norms)
        scored_keywords:list[str] = [word_index[i] for i in sorted_array if norms[i] <= avg]
        
        return vector, sentimentResults,scored_keywords 


    def _process_senti_total(self, vectorMap, vector, sentimentWordMap, sentimentRatio):
        sentimentVectors = SentinmentVector()
        for sentiment, sentimentWords in sentimentWordMap.items():
            total = sum(sentimentWords.values())
            if total == 0:
                continue 
            reguraised = {k:v / total for k, v in sentimentWords.items()}
            setattr(sentimentVectors, sentiment,  sum([vectorMap[k] * w for k, w in  reguraised.items()]))
        total = sum(sentimentRatio.values())
        sentimentWeights = SentimentWeights()
        for sentiment, weight in sentimentRatio.items():
            setattr(sentimentWeights, sentiment, weight / total)
        ret = SentimentResult()
        ret.vectors = sentimentVectors
        ret.weights = sentimentWeights

        return ret


            
   
    def _processSentiment(self, line:str, weigts:defaultdict, positionWeight:float, sentimentWordMap:dict, sentimentRatio:dict):
        sentiments = self._analizeSentiment(line)
        
        for face, weight in weigts.items():
            for sentiment, sWeight in sentiments.items():
                sentimentWordMap[sentiment][face] += weight * sWeight * positionWeight
        for sentiment, sWeight in sentiments.items():
            sentimentRatio[sentiment] += sWeight * positionWeight

            



    def _analizeSentiment(self, line):
        return self._sentimentAnalyzer.exec(line)

    def _computeWait(self, subnodes, position, nodeslen):
        weights = defaultdict(float)
        nodeWeight = 1 -  math.sin(math.pi * position / nodeslen) * 0.6 - 0.1 * position / nodeslen
        for surface, subscore in subnodes:
            weights[surface] += subscore * nodeWeight
        return weights, nodeWeight

