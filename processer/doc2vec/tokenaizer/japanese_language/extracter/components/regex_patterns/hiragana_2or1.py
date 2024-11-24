import regex as re

hiragana_2or1_pt = re.compile(r'^\p{Hiragana}{1,2}$')
