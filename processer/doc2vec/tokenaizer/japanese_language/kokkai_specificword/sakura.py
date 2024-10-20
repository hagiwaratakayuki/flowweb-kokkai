from ...extractor.fix_word import RegexExtractor
import re

extract = RegexExtractor(re.compile(r'桜を.る会'), "桜を見る会")
