import json
from functools import lru_cache

import Levenshtein


ld = lru_cache(maxsize=None)(Levenshtein.distance)


def 代价(对):
    return sum([ld(a, b) for a, b in 对])/len(对)


def load_dict(path) -> dict:
    d = {}
    with open(path, encoding='utf8') as f:
        for i in f:
            i = i.strip()
            a, b = i.split('\t')
            b = b.split(',')[0]
            assert b[0] == b[-1] == '/'
            b = b[1:-1]
            d[a] = b
    return d


英文ipa = load_dict('../not_translator/ipa_data/en_US.txt')
中文ipa = load_dict('../not_translator/ipa_data/zh_hans.txt')

英文ipa = {k.lower(): v for k, v in 英文ipa.items()}
中文ipa = {k: v.replace('˥˥', '').replace('˧˥', '').replace('˨˩˦', '').replace('˥˩', '').replace('˧', '') for k, v in 中文ipa.items() if len(k) == 1}


with open('data/名字.json', encoding='utf8') as f:
    名字对应 = json.load(f)

对 = []

for k, v in 名字对应.items():
    k = k.lower()
    真读 = 英文ipa.get(k)
    if not 真读:
        continue
    假读 = ''.join([中文ipa[x] for x in v])
    真读 = f'「{真读}」'
    假读 = f'「{假读}」'
    对.append((真读, 假读))
