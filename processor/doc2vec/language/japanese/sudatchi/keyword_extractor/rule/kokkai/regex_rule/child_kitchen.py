import re
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.component.regex import SudatchiRegexRule


rule = SudatchiRegexRule(re.compile(
    r'子ども食堂'), output_word='こども食堂', is_bind_output=True, is_force=True)
