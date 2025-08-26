from data_loader.kokkai_reguraizer import kansuuji_houritu, kyujitai, jikosyoukai, kugirisenn, unicodedata, hattaraku, kyuu_kana, child


reguraizers = [
    kugirisenn.convert,
    jikosyoukai.convert,
    unicodedata.convert,

    # kyujitai.convert,
    # hattaraku.convert,
    # kyuu_kana.convert,
    child.convert,
    kansuuji_houritu.convert,

]
