import csv
import json
import re

from collections import defaultdict
kuuhaku = re.compile('\s+[^\s]+$', re.U)

with open('../../rows/all_law_list.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    next(reader, None)

    ngram_dict = defaultdict(set)
    for row in reader:
        row = kuuhaku.sub(row, '')
        value = row[2]
        update = [value]

        for i in range(len(value)):

            key = value[i:i+2]
            ngram_dict[key].update(update)


def custom(v):
    if isinstance(v, set):
        return list(v)
    return v


with open("../processer/doc2vec/tokenaizer/japanese_language/kokkai_specificword/nameindex.json", 'w', encoding='utf-8') as f:
    json.dump(ngram_dict, f, default=custom, ensure_ascii=False)
