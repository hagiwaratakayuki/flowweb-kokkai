from .basic import RegexRemover
from .o_kanji import o_kanji

preg_remover = RegexRemover(
    [

        o_kanji,

    ]
)
