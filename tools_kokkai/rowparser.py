import csv
import json
import re

from collections import defaultdict
kuuhaku = re.compile(r'\s+[^\s]+$', re.U)


def create_dict(value, ngram_dict):
    update = [value]
    for i in range(len(value) - 1):

        key = value[i:i + 2]
        if key == '法律':
            continue
        ngram_dict[key].update(update)


with open('../../laws/all_law_list.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    next(reader, None)

    ngram_dict = defaultdict(set)
    for row in reader:
        row = kuuhaku.sub(row, '')
        value = row[2]
        create_dict(value=value)


def custom(v):
    if isinstance(v, set):
        return list(v)
    return v


with open("../processer/doc2vec/tokenaizer/japanese_language/kokkai_specificword/nameindex.json", 'w', encoding='utf-8') as f:
    json.dump(ngram_dict, f, default=custom, ensure_ascii=False)
