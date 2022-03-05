# 【not_translator】不会翻译机

英语太难了，孩子学不会，怎么办？

还好，聪明的莉沫酱发明了不会翻译机！它可以把世界上所有的语言都翻译成中文！

- 优点
    + 不依赖第三方库，可以轻松移植到网页和手机上
    + 无需网络，防止资本主义的走狗偷窥你的隐私
    + 速度快，推理时间复杂度好像是`O(n)`的<sub>(我也不确定)</sub>
    + 体积小，节省硬盘空间

- 缺点
    + 是音译


## 使用效果

我们先来翻译国家的名字吧！

```
America 
```
```
啊吗啦咖
```

看起来效果不错，我翻译的比美利坚好嘛！

<br/>

再试试俄国/德国/波兰——

```
Russia, Deutsch and Poland.
```
```
啦下, 多一起 俺得 伯懒得.
```

发音非常标准！

<br/>

好，接下来我们来翻译一些名言，先从长颈鹿开始，因为「长颈鹿是无情的动物」——
```
Giraffes are heartless creatures.
```
```
樵夫丝 二 哈特啦丝 苛礼条丝.
```

<br/>

还有「信任他人很好，但是不信任更好」——
```
It is good to trust others, but, not to do so is much better.
```
```
一得 乙巳 歌舞得 度 得啦丝特 俄饿死, 八得, 娜得 度 度 所 乙巳 吗七 八得.
```


## 原理

其实原理非常简单。因为中文是拼音拼出来的，而英文是音标拼出来的，所以只要找到它们之间的对应关系，就可以把英文翻译成中文啦。

### 机器学习

举个例子，兰斯(lance)，英语读作`/ˈɫæns/`，中文读作`lansi`。那很显然，我们只要把`ɫ`变成`l`，`æ`变成`a`，`s`变成`si`，就好了嘛！

但是这个规则往往不是那么靠谱，比如`s`显然不能都变成`si`，至少是`s`在结尾的时候才能变成`si`。以及前面的什么情况下`ɫ`变成`l`，`æ`变成`a`，也不是很好确定，所以我想，可以用机器学习来解决这个问题。

于是我收集了1300个英文人名，以及它们对应的音译，让机器从其中学习转换的规则。

我们学习的目标是得到一串转换规则，每个规则即`str.replace(a, b)`中的两个参数。

代价函数是读音经过转换后与目标的编辑距离。

那么，显然有一个非常简单的思路——就随机从英文读音中挑一个子串`a`，随机从中文读音中挑一个子串`a`，然后所有读音全部`s = s.replace(a, b)`。如果这样使代价降低了，就把这个规则保存下来，如果没有降低，就把replace操作回滚。

这样理论上是可行的，但是实际效果很差，因为收敛太慢了。

接下来我把它适当地改进一下: 

还记得我们现在的每个人名都是一个对<sub>(pair)</sub>，对吧。那现在我们让每个人名随机从它自己中挑出子串`a`和`b`，如果它自己`replace(a, b)`会让它自己的代价降低，它就会把`(a, b)`提交给议会。

每个人都提交之后，议会将最多的`(a, b)`作为这一轮的规则，把所有读音全部`s = s.replace(a, b)`。如果代价降低了，就把这个规则保存下来，如果没有降低，就把replace操作回滚，同时，直到下一个规则通过之前，不再考虑这一轮所用的规则。

嗯对，就这么简单。然后把这个代码放在宿舍里跑半天，你就可以得到一组不错的规则了。


### 动态规划

接下来，我们根据得到的规则把音标变成拼音了之后，如何把拼音还原回汉字呢？

只需要用一个简单的`O(n)`DP——

我们的目标是把一组拼音尽可能地变成汉字，也就是说，我们的目标是尽可能把拼音一字不剩地用完。

因此我们以当进行到第`i`个位置时，无法被消耗掉的拼音为代价，可以写出这样的转移方程——

```
代价[i] = min([代价[j] + f(s[j:i]) for j in range(i-k, i)])
```

其中函数`f`定义为，如果子串`s`是一个合法的拼音，返回`0`，否则返回`len(s)`。`k`为最长的拼音的长度，如果长度超过`k`，那么`s[j:i]`显然不合法。

好，就是这样，最后把方程跑过一遍，就可以把拼音还原回汉字了。


## 使用方法

首先你需要有一个Python3.7以上版本，然后把这个仓库clone回去，再`from not_translator import translate`，就行了。

<sub>好累啊我先休息一会，等下发pip包吧</sub>

接口是这样的——

```python
def translate(s: str) -> str: ...
```

## 结束

好，我回去睡觉了，大家88！
