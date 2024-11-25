from data_loader.kokkai_reguraizer import kansuuji_houritu, kyujitai, jikosyoukai, kugirisenn, unicodedata, hattaraku, kyuu_kana


reguraizers = [
    kugirisenn.convert,
    jikosyoukai.convert,
    unicodedata.convert,
    kansuuji_houritu.convert,
    kyujitai.convert,
    hattaraku.convert,
    kyuu_kana.convert


]
