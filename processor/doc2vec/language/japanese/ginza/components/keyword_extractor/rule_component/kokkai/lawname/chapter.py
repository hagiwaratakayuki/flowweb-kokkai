
from operator import is_, le
import re
from turtle import mode
from typing import List, Optional, Set, Tuple, Union, Any

from regex import T
from sklearn import base
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.dtos import LawDTOList, LawDTO
from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.types import IsCountChapterFlag, カタカナ章表現を示すフラグ
from processor.doc2vec.spacy.components.nlp.loader import load_matcher, loadnlp
スーパー301条対策のパターン = re.compile('ス.パ.')

グループ分け単語 = set('編章節款目')

章としての区分を表す単語 = r"条項号"
最大深さ = len(章としての区分を表す単語)  # 条項号+イロハ
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
    prev_match: Optional[Tuple[int, int, int]]

    def __init__(self, doc: Doc, model_name) -> None:
        self.sentence_index = -1
        self.sentence_matches_index = -1
        self.doc = doc
        matcher, vocab = get_chapter_expression_matcher(model_name)
        self.senetnce_sequence = [(sent, matcher(sent),) for sent in doc.sents]
        self.sentence_len = len(self.senetnce_sequence)
        self.vocab = vocab
        self.prev_match = None

    def step_sentence(self):
        self.sentence_index += 1
        self.prev_match = None
        self.now = None

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
            self.prev_match = self.now

            match_id, start, end = self.senetnce_matches[self.sentence_matches_len]
            now_span = self.doc[start:end]

            self.now = (self.vocab[match_id], now_span)

            return True
        return False


ChapterNodeType = Tuple[str, Optional[str]]


class ChapterPathData:
    base_path: List[ChapterNodeType]
    path: List[ChapterNodeType]
    start_level: Optional[int]
    node_count: int
    is_relative: bool

    def __init__(self, is_relative=False) -> None:
        self.base_path = []
        self.path = []
        self.start_level = None
        self.node_count = 0
        self.is_relative = is_relative

    def get_path(self):
        return self.base_path + self.path


class ChapterPath(ChapterPathData):

    def __init__(self, base_path_data: Optional[ChapterPathData] = None, is_relative: Optional[bool] = None, start_level=None, from_level: Optional[int] = None) -> None:

        if is_relative != None:
            super().__init__(is_relative=is_relative)
        else:
            super().__init__()

        if base_path_data != None:

            self.base_path = base_path_data.get_path()[:from_level]

            self.start_level = (base_path_data.start_level or 0)
            if from_level == None:
                self.start_level += base_path_data.node_count

            else:
                if from_level >= 0:
                    self.start_level = from_level - 1

                else:
                    self.start_level = self
        else:

            self.path = []
            self.is_relative = base_path_data.is_relative
        if start_level != None:
            self.start_level = start_level

    def append_node(self, chapter_count, level_expression=None):
        self.path.append((chapter_count, level_expression, ))
        self.node_count += 1

    def check_le_from_level(self, level_expression):

        level_count = 章の区分と数値の変換表.get(level_expression)
        return (self.start_level or 0) + self.node_count > level_count

    def prepend_node(self, chapter_count, level_expression=None):
        self.path.insert(0, (chapter_count, level_expression, ))

    def resolve(self):
        len_base = len(self.base_path)

        total_depth = len_base + self.node_count
        depth_diff = total_depth - 最大深さ
        if depth_diff > 0:
            chapter_path = self.base_path[:-depth_diff]
        else:
            chapter_path = self.base_path
        chapter_path.extend(self.path)
        depth = -1
        result = []
        for count_expression, level_expression in chapter_path:
            depth += 1
            if level_expression == None:
                if count_expression in カタカナ一文字:
                    level_expression = ''
                else:
                    if depth >= 最大深さ:
                        return False

                    level_expression = 章としての区分を表す単語[depth]
            else:
                estimate_depth = 章の区分と数値の変換表.get(level_expression)
                if estimate_depth == None or estimate_depth != depth:
                    return False

            result.append((count_expression, level_expression, ))
        return result

    def resolve_inversion(self, chapter_path: List):
        self.base_path = chapter_path[:].extend(self.base_path)
        self.start_level += len(chapter_path)


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
    now_chapter_path: ChapterPath = None
    chapter_paths = []
    while chapter_expression_matches.step_sentence():
        before_hit: Span = None
        while chapter_expression_matches.step_sentence_matches():

            match_id, span = chapter_expression_matches.now

            if not is_last:
                if next_law.start <= span.start_char:
                    step_success, is_last, next_law, path_index = _step_law_dto_list_with_flags(
                        law_dto_list)
            if match_id == カタカナの可能性のあるパターンのID:
                if span[0] not in カタカナ一文字:
                    continue
            elif match_id == REGULAR_PATTERN_ID:
                if span.text == "百条" and doc.text[span.start_char:span.start_char + 5] == "百条委員会":
                    continue
                if span[0].norm_ == "301" and span.start_char >= 4 and スーパー301条対策のパターン.match(doc.text[span.start_char - 4:span.start]):
                    continue

            head_token = span[0]
            is_new_path = False
            for token in span:
                _now_path = path_index.get(token, None)
                if _now_path != now_path:
                    is_new_path = True
                    now_path = _now_path
                    break

            if match_id == REGULAR_PATTERN_ID:
                chapter_expression = span[1].norm_
                if now_path == None:
                    now_chapter_path = ChapterPath()
                    chapter_paths.append(now_chapter_path)
                else:
                    if now_chapter_path.check_le_from_level(chapter_expression):
                        now_chapter_path = ChapterPath(
                            base_path_data=now_chapter_path, from_level=max(0, 章の区分と数値の変換表.get(chapter_expression, 0)))
                        chapter_paths.append(now_chapter_path)

                now_chapter_path.append_node(
                    head_token.norm_, chapter_expression)

            else:
                is_parallel = False

                if before_hit != None and before_hit[-1] == doc[head_token.i - 1] and before_hit[-1].is_punct:
                    is_parallel = True
                else:
                    check_is_parallel()
                chapter_count = head_token.norm_
                if match_id == COUNT_ONLY_PATTERN_ID:
                    level_expression = None

                elif match_id == カタカナの可能性のあるパターンのID:
                    # イ、ロ、ハ 形式
                    level_expression = ''

                if not is_parallel and (is_new_path or now_chapter_path == None):
                    now_chapter_path = ChapterPath(is_relative=True)
                elif is_parallel:
                    now_chapter_path = ChapterPath(
                        base_path_data=now_chapter_path, is_relative=True, from_level=-1)
                    chapter_paths.append(now_chapter_path)

                now_chapter_path.append_node(
                    chapter_count=chapter_count, level_expression=level_expression)


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
    group_index = {}
    group = set()
    for token in start_span:
        for ancestor in token.ancestors:

            if ancestor.i < start_span.end:
                continue
            if next_law_dto != None and ancestor.idx > next_law_dto.start:
                break

            if ancestor.pos_ in UnchangablePos or ancestor.norm_ in chapter_title_set:
                group.add(ancestor)
                group_index[ancestor] = group
                continue

            group = set()

    return group_index


並列を表す日本語のパターン = [
    'と',
    '並びに',
    'ならびに'
    '及び',
    'それと',




]


_parallel_pattern = None


def check_is_parallel(target_span: Span, model_name):
    matcher = get_parallel_matcher(model_name)
    matches = matcher(target_span)
    if len(matches) == 0:
        return False
    target_tokens = target_span[max([m[1] for m in matches]):]
    if len(target_tokens) == 0:
        return True
    for token in target_tokens:
        if not _check_is_abstract(token=token):
            return False
    return True


def get_parallel_matcher(model_name) -> Tuple[Matcher, int]:
    global _parallel_pattern
    if _parallel_pattern != None:
        return _parallel_pattern
    _parallel_pattern = _generate_check_pattern(
        並列を表す日本語のパターン, 'paralel_pattern', model_name)
    return _parallel_pattern


def _generate_check_pattern(pattern_strings, match_name, model_name):
    nlp = loadnlp(model_name)
    matcher, vocab = load_matcher(model_name)
    pattern = []
    max_token_count = 0
    for pattern_string in pattern_strings:
        parsed = nlp(pattern_string)

        pattern.append(([{"NORM": token.norm} for token in parsed]))
    matcher.add(match_name, pattern)

    return pattern, max_token_count


_non_abstract_pos = {'PROPN', 'NOUN'}
助詞のと句読点または第 = {'の、', 'の第'}
助詞のと句読点と第 = 'の、第'


def check_inverse_exception(base_span: Span, end_id: int, sentence: Span, doc: Doc, ):
    target_span = doc[base_span.end + 1:end_id + 1]

    target_span_len = len(target_span)

    if target_span_len == 1:
        return sentence.end == end_id and target_span.text == 'の'
    if target_span_len == 2 and target_span.text in 助詞のと句読点または第:
        return False
    if target_span_len == 3 and target_span.text == 助詞のと句読点と第:
        return False
    助詞のが無くてもいいかのフラグ = False

    base_head = base_span[0]

    if base_head.id >= 2:
        first_back_token = doc[base_head.i - 1]
        second_back_token = doc[base_head.i - 2]
        助詞のが無くてもいいかのフラグ = (first_back_token.is_punct or first_back_token.pos_ ==
                           "ADP") and second_back_token.pos_ == "PRON"
        助詞のが無くてもいいかのフラグ |= first_back_token.pos_ == "PRON"

    is_first = True
    のが見つかったか = False
    for target_token in target_span:
        if not is_first and target_token.is_punct:
            break
        is_first = False
        のが見つかったか |= target_token.norm_ == 'の'
        if target_token.pos_ in _non_abstract_pos:
            return False

    return のが見つかったか or 助詞のが無くてもいいかのフラグ


def _check_is_abstract(token: Token):
    return token.pos_ == 'PROPN' or (token.pos_ == 'NOUN' and token.tag_.index('数詞') == -1 and token.norm_.index('気') != 0)
