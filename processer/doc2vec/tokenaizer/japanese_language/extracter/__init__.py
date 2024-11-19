from .kokkai_specificword import lowname, super_301, sakura
from . basic import complex_word, sahen


rule_extractor = [

    lowname.extract,
    super_301.extract,
    sakura.extract,
    complex_word.extract,
    sahen.extract

]
