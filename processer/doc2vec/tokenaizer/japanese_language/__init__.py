from doc2vec.tokenaizer.japanese_language import nonkana, sahen
from doc2vec.tokenaizer.japanese_language.kokkai_specificword import lowname

rule_extractor = [
    nonkana.extract,
    lowname.extract,
    sahen.extract

]
