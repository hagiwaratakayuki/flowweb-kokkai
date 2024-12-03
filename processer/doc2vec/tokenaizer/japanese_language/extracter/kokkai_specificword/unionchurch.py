from ....extractor.fix_word import RegexExtractor
import re

extract = RegexExtractor(re.compile(r'旧?統一[協教]会|世界平和統一家庭連合'), [
                         "統一教会", "統一協会", "世界平和統一家庭連合"])
