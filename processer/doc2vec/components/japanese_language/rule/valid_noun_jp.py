import regex as re
from doc2vec.components.japanese_language.regex_patterns import hiragana_include
from doc2vec.components.japanese_language.regex_patterns import noun_blockpattern
# MeCabとデフォルト辞書の旧字体及び「つ」カウント(一つとか)、話し言葉の間投詞的(皆様、等々など)表現対策 + 子ども(子供・こども)の統一


def check_valid_noun(face: str):
    return face == "子ども" or (hiragana_include.pattern.search(face) is None and noun_blockpattern.compiled.search(face) is None)
