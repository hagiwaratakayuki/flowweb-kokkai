from ....extractor.fix_word import RegexExtractor
import re

extract = RegexExtractor(re.compile(r'旧?統一[協教]会|世界平和統一家庭連合|世界基督教統一神霊協会|(世界)?(平和)?(統一)?家庭連合'), [
                         "統一教会", "統一協会", "世界平和統一家庭連合"], headword="統一")
