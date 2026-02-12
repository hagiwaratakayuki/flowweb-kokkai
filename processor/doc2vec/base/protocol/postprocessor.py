from typing import Any, Iterable, Tuple
from abc import ABCMeta, abstractmethod

from numpy import ndarray

from data_loader.dto import DTO

from doc2vec.base.protocol.sentiment import SentimentAnarizer, SentimentResult
from doc2vec.base.protocol.vectorizer import WordVectorizer
from .tokenizer import TokenDTO


DocVectorType = ndarray
KeywordsType = Iterable[str]
ExecResponseType = Tuple[DocVectorType, SentimentResult, KeywordsType, DTO]


class AbstractPostprocessorCls(metaclass=ABCMeta):
    @abstractmethod
    def exec(self, token_dto: TokenDTO, dto: Any) -> ExecResponseType:
        pass


class PostprocessorBase(AbstractPostprocessorCls):
    sentiment_anaraizer: SentimentAnarizer
    vectorizer: WordVectorizer
