def convert(text: str, speechData):

    splited = text.split('。')
    firstline = splited[0]
    speaker = speechData.get('speaker', '')
    is_jikosyoukai = False
    l = len(speaker)
    for i in range(0, l):
        needle = speaker[0:l - i]
        if needle in firstline:
            is_jikosyoukai = True
    if is_jikosyoukai is True:
        splited.pop(0)
    return '。'.join(splited)
