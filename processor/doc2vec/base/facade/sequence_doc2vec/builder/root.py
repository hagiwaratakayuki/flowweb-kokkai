from typing import Dict, List, Type
from doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter
from doc2vec.base.builder.components.mixins.use_filter import UseFilterMixin
from doc2vec.base.keyword_extractor.basic import BasicKeywordExtractor
from doc2vec.base.protocol.document_vectoraizor import AbstractDocumentVectoraizer
from doc2vec.base.protocol.tokenizer import AbstarctTokenizerClass


class SequenceDoc2VecBuilderRoot:
    keyword_extractor_class: Type[BasicKeywordExtractor] = BasicKeywordExtractor
    keyword_extractor_params: Dict
    tokenaier_class: Type[AbstarctTokenizerClass]
    tokenaier_params: Dict
    document_vectoraizer_class: Type[AbstractDocumentVectoraizer]
    document_vectoraier_params: Dict
