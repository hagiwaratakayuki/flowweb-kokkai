from doc2vec.tokenaizer.japanese_language import nonkana, sahen
from doc2vec.tokenaizer.japanese_language.kokkai_specificword import lowname, super_301, sakura

rule_extractor = [

    lowname.extract,
    super_301.extract,
    sakura.extract,
    nonkana.extract,
    sahen.extract

]
