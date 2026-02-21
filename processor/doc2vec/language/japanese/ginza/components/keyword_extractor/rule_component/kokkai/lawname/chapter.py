
import re
from typing import List, Optional, Set, Tuple, Union, Any

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.dtos import LawDTOList, LawDTO
from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.types import IsCountChapterFlag, カタカナ章表現を示すフラグ
from processor.doc2vec.spacy.components.nlp.loader import load_matcher, loadnlp
スーパー301条対策のパターン = re.compile('ス.パ.')

グループ分け単語 = set('編章節款目')

章としての区分を表す単語 = r"条項号"
章の区分と数値の変換表 = {章としての区分を表す単語[i]: i for i in range(len(章としての区分を表す単語))}
カタカナ一文字 = {'イ', 'ロ', 'ハ', 'ニ', 'ホ', 'ヘ', 'ト', 'チ', 'リ', 'ヌ', 'ル', 'ヲ', 'ワ', 'カ', 'ヨ', 'タ', 'レ', 'ソ', 'ツ', 'ネ', 'ナ', 'ラ', 'ム',
           'ウ', 'ヰ', 'ノ', 'オ', 'ク', 'ヤ', 'マ', 'ケ', 'フ', 'コ', 'エ', 'テ', 'ア', 'サ', 'キ', 'ユ', 'メ', 'ミ', 'シ', 'ヱ', 'ヒ', 'モ', 'セ', 'ス', 'ン'}
chapter_title_set = set(章としての区分を表す単語)
章とグループ分けの単語 = chapter_title_set | グループ分け単語 | カタカナ一文字

chapter_expression_matcher: Optional[Matcher] = None
vocab = None


REGULAR_PATTERN_ID = "regular_pattern"
COUNT_ONLY_PATTERN_ID = "count_only_pattern"
カタカナの可能性のあるパターンのID = "カタカナの可能性のあるパターン"


def get_chapter_expression_matcher(model_name):
    global chapter_expression_matcher, vocab
    if chapter_expression_matcher != None:
        return chapter_expression_matcher, vocab
    _chapter_expression_matcher, _vocab = load_matcher(model_name)
    regular_pattern = [
        [{"POS": "NUM"}, {"TEXT": {"IN": list(章としての区分を表す単語)}}]
    ]

    _chapter_expression_matcher.add(REGULAR_PATTERN_ID, regular_pattern)
    count_only_pattern = [
        [{"POS": "NUM"}, {"POS": "ADP"}],
        [{"POS": "NUM"}, {"POS": "PUNCT"}],
        [{"POS": "NUM"}, {"POS": "AUX"}]
    ]
    _chapter_expression_matcher.add(COUNT_ONLY_PATTERN_ID, count_only_pattern)
    カタカナの可能性のあるパターン = [
        [{"LENGTH": 1}, {"POS": "ADP"}],
        [{"LENGTH": 1}, {"POS": "PUNCT"}],
        [{"LENGTH": 1}, {"POS": "AUX"}]
    ]
    _chapter_expression_matcher.add(
        カタカナの可能性のあるパターンのID, カタカナの可能性のあるパターン)
    chapter_expression_matcher = _chapter_expression_matcher
    vocab = _vocab
    return _chapter_expression_matcher, _vocab


class ChapterExpressionMatches:
    senetnce_sequence: List[Span, Tuple[List[Tuple[int, int, int]]]]
    sentence_index: int
    sentence_len: int
    sentence_matches_index: int
    sentence_matches: List[Tuple[int, int, int]]
    sentence_matches_len: int
    sentence_now: Span
    doc: Doc
    now: Tuple[str, Span]
    vocab: Any

    def __init__(self, doc: Doc, model_name) -> None:
        self.sentence_index = -1
        self.sentence_matches_index = -1
        self.doc = doc
        matcher, vocab = get_chapter_expression_matcher(model_name)
        self.senetnce_sequence = [(sent, matcher(sent),) for sent in doc.sents]
        self.sentence_len = len(self.senetnce_sequence)
        self.vocab = vocab

    def step_sent(self):
        self.sentence_index += 1

        if self.sentence_index < self.sentence_len:

            self.sentence_matches_index = -1
            now, matches = self.senetnce_sequence[self.sentence_index]
            self.sentence_matches = matches
            self.sentence_matches_len = len(self.sentence_matches)
            self.sentence_now = now

            return True
        return False

    def step_sentence_matches(self):
        self.sentence_matches_index += 1
        if self.sentence_matches_index < self.sentence_matches_len:

            match_id, start, end = self.senetnce_matches[self.sentence_matches_len]
            now_span = self.doc[start:end]

            self.now = (self.vocab[match_id], now_span)

            return True
        return False

# 倒置表現対応。数値のみ場合は数値トークン、イロハ表記の場合はイロハ、条項トークンがついている場合は条項トークンからたどって倒置先の条項トークンまたは法律に繋がれば倒置＝待機


def extract_chapter_expressions(doc: Doc, law_dto_list: LawDTOList, model_name):
    law_dto_list.rewind()
    step_success, is_last, next_law, path_index = _step_law_dto_list_with_flags(
        law_dto_list)
    if not step_success:
        return

    chapter_expression_matches = ChapterExpressionMatches(
        doc=doc, model_name=model_name)
    now_path: Optional[Set[Token]] = None
    while chapter_expression_matches.step_sent():
        while chapter_expression_matches.step_sentence_matches():
            match_id, span = chapter_expression_matches.now

            if not is_last:
                if next_law.start <= span.start_char:
                    step_success, is_last, next_law, path_index = _step_law_dto_list_with_flags(
                        law_dto_list)
            if match_id == カタカナの可能性のあるパターンのID and span[0] not in カタカナ一文字:
                continue
            if match_id == REGULAR_PATTERN_ID:
                if span.text == "百条" and doc.text[span.start_char:span.start_char + 5] == "百条委員会":
                    continue
                if span[0].norm_ == "301" and span.start_char >= 4 and スーパー301条対策のパターン.match(doc.text[span.start_char - 4:span.start]):
                    continue

            # TODO 段階の深さが違った場合、あるいはあるいは相対表記の途中で登場した場合の処理を実装
            if match_id == REGULAR_PATTERN_ID:

                num = span[0].norm_
                word = span[1].text
                law_dto_list.now.chapter_canditates.append(
                    (IsCountChapterFlag, num, word))

            elif match_id == COUNT_ONLY_PATTERN_ID:
                # 『○○の1、」みたいなパターン
                is_new_path = False
                for token in span:
                    _now_path = path_index.get(token, None)
                    if _now_path != now_path:
                        is_new_path = True
                        now_path = _now_path
                        break
                if not is_new_path:

                    pass

                else:
                    pass

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
    step_success = law_dto_list.step()
    is_last = False
    next_law = None
    if not step_success:
        return step_success, is_last, next_law

    is_last = law_dto_list.is_last()
    next_law = None
    if not is_last:
        next_law = law_dto_list.get_next()
    path_index = {}
    if law_dto_list.now.is_guess == False:
        path_index = _generate_path_index(
            law_dto_list.now.tokens, next_law)
    return step_success, is_last, next_law, path_index


UnchangablePos = {"NUM", "PUNCT"}


def _generate_path_index(start_span: Span, next_law_dto: Optional[LawDTO]):
    path_index = {}
    path = set()

    for token in start_span:
        for ancestor in token.ancestors:

            if ancestor.i < start_span.end:
                continue
            if next_law_dto != None and ancestor.idx > next_law_dto.start:
                break

            if ancestor.pos_ in UnchangablePos or ancestor.norm_ in chapter_title_set:
                path.add(ancestor)
                path_index[ancestor] = path
                continue

            path = set()

    return path_index


並列を表す日本語のパターン = [
    'と',
    '並びに',
    'ならびに',
    '及び',
    'それと'



]


def _generate_check_pattern(pattern_strings: List[str], model_name, precondition=None, postcondition=None):
    nlp = loadnlp(model_name)
    pattern = []
    for pattern_string in pattern_strings:
        parsed = nlp(pattern_string)
        conditions = []
        if precondition != None:
            conditions.append(precondition)
        for token in parsed:
            conditions.append({'NORM': token.norm_})
        if postcondition != None:
            conditions.append(postcondition)
        pattern.append(conditions)
    return pattern
