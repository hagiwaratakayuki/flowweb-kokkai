

from doc2vec.language.japanese.sudatchi.keyword_extractor.rule import base
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.kokkai import lawname, regex_rule


rule = base.rules + regex_rule.rules + [
    lawname.Rule()
]

stopword_rules = []
