from .basic import RegexRemover
from .ichimoji import itchimoji
from .o_kanji import o_kanji
from .kyuujitai_brokun import kyuujitai_broken
preg_remover = RegexRemover(
    [
        itchimoji,
        o_kanji,
        kyuujitai_broken
    ]
)
