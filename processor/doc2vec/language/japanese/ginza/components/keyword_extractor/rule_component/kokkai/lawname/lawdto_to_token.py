
from ast import List
from collections import defaultdict
from typing import DefaultDict, Dict, Set
from spacy.tokens import Doc, Token, Span
from .dtos import LawDTO, LawDTOList


def link_law_and_token(doc: Doc, law_dto_list: LawDTOList):
    law_dto_list.rewind()
    token_to_law: Dict[Token, LawDTO] = {}

    lawname_to_token: DefaultDict[str, Set[Token]] = defaultdict(set)

    while law_dto_list.step():
        law_dto = law_dto_list.now
        if law_dto.is_guess:
            continue
        span = doc.char_span(law_dto.start, law_dto.end)

        if span == None:
            continue
        law_dto.tokens = span

        for token in span:

            token_to_law[token] = law_dto
            lawname_to_token[law_dto.name].add(token)
    return token_to_law, lawname_to_token
