from collections import defaultdict, deque

import re
from typing import List
import numpy as np

from data_loader.kokkai import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.spacy.japanese_language.components.keyword_extract.util.tag_check import is_popular_noun
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.keyword_extractor.protocol import ExtractResultDTO, KeywordExtractRule
from spacy.tokens import Doc, Token, Span
from .discussion_context import DiscussionContext

会で終わるパターン = re.compile('会$')
委員会 = "委員会"
委員会の略称のパターン = [
    (re.compile('地.?こ.?デジ特.?委(員会)?'), '地域活性化・こども政策・デジタル社会形成に関する特別委員会', ),
    (re.compile('地デジ特.?委(員会)?'), '地方創生及びデジタル社会の形成等に関する特別委員会', ),
    (re.compile('拉致(問題)?特?別?委(員会)?'), '')
]


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO):
        before_chunks: List[Span] = []
        before_chunks_len = 0
        committies = defaultdict(set)
        for noun_chunk in doc.noun_chunks:

            if not 会で終わるパターン.search(noun_chunk.text):
                before_chunks.append(noun_chunk)
                before_chunks_len += 1
                continue
            if doc[noun_chunk.end].norm_ is 委員会:
                is_popular_noun_exist = False
                for token in chunk:
                    if token.i == chunk.end:
                        break
                    is_popular_noun_exist |= is_popular_noun.check(token=token)
                    if is_popular_noun_exist:
                        break
                if not is_popular_noun_exist:
                    is_exist_context, data = self.context.get_data(dto=dto)
                    if is_exist_context:
                        committies[data].add(doc[chunk.end])
                    continue

            chunks = deque([noun_chunk])
            target: Span = noun_chunk
            is_check = True
            is_cc_exist = False
            while is_check:
                header = doc[target.start]
                if (header.pos_ == 'CCONJ' or header.dep_ == 'cc'):
                    if before_chunks_len == 0:

                        break

                    is_cc_exist = True
                    target_ = before_chunks.pop()
                    before_chunks_len -= 1
                    if target_.end + 1 != target.start:

                        break
                    chunks.appendleft(target_)
                    target = target_
                    continue
                is_check = False
            if is_cc_exist:
                before_chunks = []
                before_chunks_len = 0

            committie_name = ''
            tokens = deque()
            is_check_noun = True
            for chunk in chunks:
                if is_check_noun:
                    if is_check_noun:

                        for token in chunk:
                            if is_check_noun and token.pos_ != 'NOUN':

                                continue
                            is_check_noun = False
                            tokens.append(token)
                            committie_name += token.lemma_
                else:
                    committie_name += chunk.text
                    tokens.extend(chunk)
            committies[committie_name].update(tokens)
            self.context.set_data(committie_name, dto=dto)
        for committie_name, tokens in committies.items():
            sk = SpecifiedKeyword(headword=committie_name,
                                  tokens=tokens, is_force=True)
            results.add_keyword(sk)
        return results
