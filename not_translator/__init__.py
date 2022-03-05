import re
import json
import math
from pathlib import Path
from collections import Counter


here = Path(__file__).parent

with open(here/'摸型.json', 'r', encoding='utf8') as f:
    模型 = json.load(f)
with open(here/'常用汉字.json', encoding='utf8') as f:
    常用汉字 = {*json.load(f)}


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


英文ipa = load_dict(here/'ipa_data/en_US.txt')
中文ipa = load_dict(here/'ipa_data/zh_hans.txt')

英文ipa = {k.lower(): v for k, v in 英文ipa.items()}
中文ipa = {k: v.replace('˥˥', '').replace('˧˥', '').replace('˨˩˦', '').replace('˥˩', '').replace('˧', '').replace(' ', '') for k, v in 中文ipa.items()}


def 转移(s, 风):
    l = []
    源a = f'「{英文ipa[s]}」'
    for f in 风:
        a = 源a
        for x, y in f:
            a = a.replace(x, y)
        l.append(a.replace('「', '').replace('」', ''))
    return l


反向索引 = {}
for k, v in 中文ipa.items():
    if k in 常用汉字:
        反向索引.setdefault(v, k)
for k, v in 中文ipa.items():
    反向索引.setdefault(v, k)
反向索引['ða'] = 反向索引['la']  # 手动修复
k = max([len(i) for i in 反向索引])


def dp(s: str):
    n = len(s)
    代价 = [0] + [math.inf] * n
    记录 = [''] + ['?'] * n
    for i in range(n+1):
        for j in range(max(0, i-k), i):
            if s[j:i] in 反向索引:
                if 代价[j] < 代价[i]:
                    代价[i] = 代价[j]
                    记录[i] = 记录[j] + 反向索引[s[j:i]]
            else:
                if 代价[j]+(i-j) < 代价[i]:
                    代价[i] = min(代价[i], 代价[j]+(i-j))
                    记录[i] = 记录[j] + s[j:i]
    return 记录[-1], 代价[-1]


def 真移(s):
    s = s.lower()
    if s not in 英文ipa:
        return s
    l = [i[0] for i in Counter(转移(s, 模型)).most_common(9)]
    for x in l:
        z, w = dp(x)
        if w == 0:
            return z
    return dp(l[0])[0]


def translate(s: str) -> str:
    return re.sub('[a-zA-Z]+', lambda x: 真移(x.group()), s)
