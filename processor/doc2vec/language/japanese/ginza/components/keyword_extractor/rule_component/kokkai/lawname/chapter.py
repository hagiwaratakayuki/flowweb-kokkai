import re
from typing import List, Optional, Tuple, Union, Any
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.dtos import LawDTOList
from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.types import IsCountChapterFlag, カタカナ章表現を示すフラグ
from processor.doc2vec.spacy.components.nlp.loader import load_matcher
スーパー301条対策のパターン = re.compile('ス.パ.')

章としての区分を表す単語 = r"条項号"
章の区分と数値の変換表 = {章としての区分を表す単語[i]: i for i in range(len(章としての区分を表す単語))}
カタカナ一文字 = {'イ', 'ロ', 'ハ', 'ニ', 'ホ', 'ヘ', 'ト', 'チ', 'リ', 'ヌ', 'ル', 'ヲ', 'ワ', 'カ', 'ヨ', 'タ', 'レ', 'ソ', 'ツ', 'ネ', 'ナ', 'ラ', 'ム',
           'ウ', 'ヰ', 'ノ', 'オ', 'ク', 'ヤ', 'マ', 'ケ', 'フ', 'コ', 'エ', 'テ', 'ア', 'サ', 'キ', 'ユ', 'メ', 'ミ', 'シ', 'ヱ', 'ヒ', 'モ', 'セ', 'ス', 'ン'}
chapter_expression_matcher: Optional[Matcher] = None
vocab = None
chapter_title_set = set(章としての区分を表す単語)

REGULAR_PATTERN_ID = "regular_pattern"
COUNT_ONLY_PATTERN_ID = "count_only_pattern"
カタカナの可能性のあるパターンのID = "カタカナの可能性のあるパターン"


def get_chapter_expression_matcher(model_name):
    global chapter_expression_matcher, vocab
    if chapter_expression_matcher != None:
        return chapter_expression_matcher, vocab
    chapter_expression_matcher = load_matcher(model_name)
    regular_pattern = [
        [{"POS": "NUM"}, {"TEXT": {"IN": list(章としての区分を表す単語)}}]
    ]

    chapter_expression_matcher.add(REGULAR_PATTERN_ID, regular_pattern)
    count_only_pattern = [
        [{"POS": "NUM"}, {"POS": "ADP"}],
        [{"POS": "NUM"}, {"POS": "PUNCT"}],
        [{"POS": "NUM"}, {"POS": "AUX"}]
    ]
    chapter_expression_matcher.add(COUNT_ONLY_PATTERN_ID, count_only_pattern)
    カタカナの可能性のあるパターン = [
        [{"LENGTH": 1}, {"POS": "ADP"}],
        [{"LENGTH": 1}, {"POS": "PUNCT"}],
        [{"LENGTH": 1}, {"POS": "AUX"}]
    ]
    chapter_expression_matcher.add(
        カタカナの可能性のあるパターンのID, カタカナの可能性のあるパターン)

    return chapter_expression_matcher, vocab


class ChapterExpressionMatches:
    index: int
    sequence: List[Tuple[int, int, int]]
    len: int
    doc: Doc
    now: Tuple[str, Span, Union[Token, False]]
    vocab: Any

    def __init__(self, doc, model_name) -> None:
        self.index = -1
        self.doc = doc
        matcher, vocab = get_chapter_expression_matcher(model_name)
        self.sequence = matcher(doc)
        self.len = len(self.sequence)
        self.vocab = vocab

    def step(self):
        self.index += 1
        if self.index < self.len:
            match_id, start, end = self.sequence[self.index]
            now_span = self.doc[start:end]
            next_token = self.doc[end]
            self.now = (self.vocab[match_id], now_span, next_token, )

            return True
        return False


def extract_chapter_expressions(doc: Doc, law_dto_list: LawDTOList, model_name):
    law_dto_list.rewind()
    has_next, is_last, next_law = _step_law_dto_list_with_flags(
        law_dto_list)
    if not has_next:
        return
    chapter_expression_matches = ChapterExpressionMatches(
        doc=doc, model_name=model_name)

    while chapter_expression_matches.step():
        match_id, span, next_token = chapter_expression_matches.now

        if not is_last:
            if next_law.start <= span.start_char:
                has_next, is_last, next_law = _step_law_dto_list_with_flags(
                    law_dto_list)
        if match_id == カタカナの可能性のあるパターンのID and span[0] not in カタカナ一文字:
            continue
        if match_id == REGULAR_PATTERN_ID:
            if span.text == "百条" and doc.text[span.start_char:span.start_char + 5] == "百条委員会":
                continue
            if span[0].norm_ == "301" and span.start_char >= 4 and スーパー301条対策のパターン.match(doc.text[span.start_char - 4:span.start]):
                continue

        # TODO 章段階の判定と並列、倒置判定を実装
        if match_id == REGULAR_PATTERN_ID:

            num = span[0].norm_
            word = span[1].text
            law_dto_list.now.chapter_canditates.append(
                (IsCountChapterFlag, num, word))

        elif match_id == COUNT_ONLY_PATTERN_ID:
            # 『○○の1、」
            num = span[0].norm_
            law_dto_list.now.chapter_canditates.append(
                (IsCountChapterFlag, num, False))

        elif match_id == カタカナの可能性のあるパターンのID:
            # イ、ロ、ハ 形式
            char = span[0].text
            if not char in カタカナ一文字:
                continue
            law_dto_list.now.chapter_canditates.append(
                (カタカナ章表現を示すフラグ, char))


def _step_law_dto_list_with_flags(law_dto_list: LawDTOList):
    has_next = law_dto_list.step()
    is_last = False
    next_law = None
    if not has_next:
        return has_next, is_last, next_law

    is_last = law_dto_list.is_last()
    next_law = None
    if not is_last:
        next_law = law_dto_list.get_next()

    return has_next, is_last, next_law
