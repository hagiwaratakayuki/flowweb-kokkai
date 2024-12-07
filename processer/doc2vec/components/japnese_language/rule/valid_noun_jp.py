import regex as re

# MeCabとデフォルト辞書の旧字体及び「つ」カウント(一つとか)対策

hiragana_2or1_pt = re.compile(r'^\p{Hiragana}{1,2}$')


def check_valid_noun(face: str):
    return hiragana_2or1_pt.search(face) is None and face[-1] != 'つ'
