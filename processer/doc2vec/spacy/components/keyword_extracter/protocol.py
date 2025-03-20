from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Optional, Set, Union
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction

type TokenID2Keyword = Dict[any, Dict[Any, SpecifiedKeyword]]


EMPTY_SET = set()


class ExtractResultDTO:
    token_id_2_keyword: TokenID2Keyword
    keywords: Dict[any, SpecifiedKeyword]

    def __init__(self):
        self.token_id_2_keyword = defaultdict(dict)
        self.keywords = {}

    def add_keyword(self, keyword: SpecifiedKeyword, is_overwrite_token=True):
        self.keywords[keyword.id] = keyword
        if is_overwrite_token == True:

            for source_id in keyword.source_ids:
                source_id_set = {source_id}
                for target_keyword in self.token_id_2_keyword.get(source_id, {}).values():

                    target_keyword.source_ids -= source_id_set
                self.token_id_2_keyword[source_id][keyword.id] = keyword
        else:
            for source_id in keyword.source_ids:
                self.token_id_2_keyword[source_id][keyword.id] = keyword

    def get_keywords(self):
        # refarence shortcut
        return [keyword for keyword in self.keywords.values() if keyword.source_ids != EMPTY_SET]

    def get_by_source_ids(self, source_ids: Iterable[Any]):
        ret: Dict[Any, SpecifiedKeyword] = {}
        for source_id in source_ids:
            ret.update(self.token_id_2_keyword.get(source_id, {}))
        return ret

    def check_by_source_ids(self, source_ids):
        return {source_id for source_id in source_ids if source_id in self.token_id_2_keyword}

    def substruct_sorce_id(self, keyword: SpecifiedKeyword, source_ids: Set[Any]):
        self.keywords[keyword.id].source_ids -= source_ids

    def remove_keyword(self, keyword: SpecifiedKeyword):
        for source_id in keyword.source_ids:
            self.token_id_2_keyword[source_id][keyword.id].source_ids -= source_id

    def overwrite_keyword(self, targets: Union[Iterable[SpecifiedKeyword], SpecifiedKeyword], keyword: SpecifiedKeyword):
        if not isinstance(targets, Iterable):
            targets = [targets]
        for target in targets:
            self.keywords[target.id].source_ids -= keyword.source_ids
        self.keywords[keyword.id] = keyword

    def add_tokens(self, keyword: SpecifiedKeyword, tokens):
        keyword.source_ids &= tokens
        for token in tokens:
            self.token_id_2_keyword[token][keyword.id] = keyword


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        pass
