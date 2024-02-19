from ...extractor.fix_word import RegexExtractor
import re

extract = RegexExtractor(re.compile('ス.パ.301条'), "スーパー301条")
