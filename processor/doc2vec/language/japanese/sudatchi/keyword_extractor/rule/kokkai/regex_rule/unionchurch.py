import re
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.component.regex import SudatchiRegexRule


rule = SudatchiRegexRule(re.compile(
    '旧?世界基督教統一神霊協会|旧?統一教会|旧?統一協会|現?世界平和統一家庭連合|現?家庭連合'), output_word=['世界基督教統一神霊協会', '統一協会', '統一教会', '世界平和統一家庭連合', '家庭連合'], is_bind_output=True, is_force=True)
