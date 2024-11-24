import re
kigou_pt = re.compile(r'^\W+$')

#  括弧や句点を除いた記号を抽出
#  dataはMecabの品詞情報


def check_symbol_without_bracket(face, data):
    return check_symbol(face) and check_is_bracket(data=data)


def check_is_bracket(data):
    return data[1] == '括弧開' or data[1] == '括弧閉' or data[1] == 'サ変接続' or data[1] == '句点'


def check_symbol(face):
    return kigou_pt.search(face) is not None
