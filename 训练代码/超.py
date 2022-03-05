import time
import json
from functools import lru_cache
import random
from typing import List, Optional, Tuple

from 数据 import 对, 代价
from collections import Counter

import Levenshtein

ld = lru_cache(maxsize=None)(Levenshtein.distance)


@lru_cache(maxsize=None)
def 破碎(s, l) -> Tuple[str, ...]:
    a = []
    for q in range(0, len(s)+1):
        for w in range(q+1, len(s)+1):
            if w-q <= l:
                a.append(s[q:w])
    return tuple(a)


def 引力(a, b) -> Optional[Tuple[str, str]]:
    if a == b:
        return None
    l = ld(a, b)
    aa = 破碎(a, 3)
    bb = 破碎(b, 3) + (' ',)
    x = random.choice(aa)
    y = random.choice(bb)
    for _ in range(10):
        if ld(a.replace(x, y), b) < l:
            return (x, y)
    return None


def 收(对) -> List:
    a = [引力(a, b) for a, b in 对]
    return [i for i in a if i]

print(对)
exit()


超录 = []
当前代价 = 代价(对)
否决 = set()
while True:
    c = Counter()
    while True:
        s = [i for i in 收(对) if i not in 否决]
        c.update(s)
        (x, y), t = Counter(c).most_common(1)[0]
        if t > 5:
            break
    新对 = [(a.replace(x, y), b) for a, b in 对]
    新代价 = 代价(新对)
    if 新代价 >= 当前代价:
        否决.add((x, y))
        print(f'否决{x}-{y}, 当前代价={当前代价}, 新代价={新代价}')
    else:
        对 = 新对
        当前代价 = 代价(对)
        否决 = set()
        print(f'通过{x}-{y}，当前代价={当前代价}')
        超录.append((x, y))
        with open(f'超录/{str(新代价)[:6]+"_"+str(random.randint(11, 99))}.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(超录, ensure_ascii=False))
