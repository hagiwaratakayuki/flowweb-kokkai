import csv
import json
import re
import unicodedata
from collections import defaultdict
kuuhaku = re.compile(r'\s+[^\s]+$', re.U)
追加の法律のリスト = [
    "同和対策事業特別措置法",
    "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律",
    "活動火山周辺地域における避難施設等の整備等に関する法律"
]
特別措置法 = "特別措置法"


def create_dict(value, ngram_dict):
    update = [value]
    for i in range(len(value) - 1):

        key = value[i:i + 2]
        if key == '法律' or key in 特別措置法:
            continue
        ngram_dict[key].update(update)


def custom(v):
    if isinstance(v, set):
        return list(v)
    return v


with open('../../laws/all_law_list.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    next(reader, None)

    ngram_dict = defaultdict(set)
    for row in reader:
        row = [unicodedata.normalize(
            'NFKC', r.replace("抄", "").strip()) for r in row]
        value = row[2]
        create_dict(value=value, ngram_dict=ngram_dict)


with open("../processer/doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/nameindex.json", 'w', encoding='utf-8') as f:
    json.dump(ngram_dict, f, default=custom, ensure_ascii=False)
