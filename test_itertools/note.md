# 无穷迭代器

|                            迭代器                            | 实参          | 作用              | 结果                                  | 示例                                    |
| :----------------------------------------------------------: | :------------ | ----------------- | :------------------------------------ | :-------------------------------------- |
| [`count()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.count) | start, [step] | 无限产出item      | start, start+step, start+2*step, ...  | `count(10) --> 10 11 12 13 14 ...`      |
| [`cycle()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.cycle) | p             | 循环产出p中的元素 | p0, p1, ... plast, p0, p1, ...        | `cycle('ABCD') --> A B C D A B C D ...` |
| [`repeat()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.repeat) | elem [,n]     | 重复elem次数      | elem, elem, elem, ... 重复无限次或n次 | `repeat(10, 3) --> 10 10 10`            |

# 有限

|                            迭代器                            | 实参                        | 作用                                                         | 结果                                             | 示例                                                       |
| :----------------------------------------------------------: | :-------------------------- | ------------------------------------------------------------ | :----------------------------------------------- | ---------------------------------------------------------- |
| [`accumulate()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.accumulate) 积累的意思 | p [,func]                   | 依次累加元素的结果                                           | p0, p0+p1, p0+p1+p2, ...                         | `accumulate([1,2,3,4,5]) --> 1 3 6 10 15`                  |
| [`chain()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.chain) | p, q, ...                   | 拼接可迭代对象                                               | p0, p1, ... plast, q0, q1, ...                   | `chain('ABC', 'DEF') --> A B C D E F`                      |
| [`chain.from_iterable()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.chain.from_iterable) | iterable -- 可迭代对象      | 基本同上，除参数类型不同，是Iterable[Iterable]               | p0, p1, ... plast, q0, q1, ...                   | `chain.from_iterable(['ABC', 'DEF']) --> A B C D E F`      |
| [`compress()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.compress) | data, selectors             | 对selector为真的返回对应位置的data                           | (d[0] if s[0]), (d[1] if s[1]), ...              | `compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F`            |
| [`dropwhile()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.dropwhile)可对比takewhile | pred, seq                   | 抛弃pred失败保留之后的结果（抛弃xxx当满足xx条件时)           | seq[n], seq[n+1], ... 从pred首次真值测试失败开始 | `dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1`          |
| [`filterfalse()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.filterfalse)可对比filter | pred, seq                   | 根据falsa来过滤                                              | seq中pred(x)为假值的元素，x是seq中的元素。       | `filterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8`      |
| [`groupby()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.groupby) | iterable[, key]             | 默认根据相等元素分组，返回(结果，分组后结果对应的元素迭代器) | 根据key(v)值分组的迭代器                         |                                                            |
| [`islice()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.islice) | seq, [start,] stop [, step] |                                                              | seq[start:stop:step]中的元素                     | `islice('ABCDEFG', 2, None) --> C D E F G`                 |
| [`starmap()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.starmap)可对比map | func, seq                   | 作用和map基本一致，除了接口不同                              | func(*seq[0]), func(*seq[1]), ...                | `starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000`       |
| [`takewhile()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.takewhile)可对比dropwhile | pred, seq                   | (拿走xxx当xx条件时)保留pred成功的直到pred失败                | seq[0], seq[1], ..., 直到pred真值测试失败        | `takewhile(lambda x: x<5, [1,4,6,4,1]) --> 1 4`            |
| [`tee()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.tee) | it, n                       | 对这个可迭代对象copy为n份可迭代器对象(**注意python中因为相同指向对象而导致的问题**) | it1, it2, ... itn 将一个迭代器拆分为n个迭代器    |                                                            |
| [`zip_longest()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.zip_longest)可对比zip | p, q, ...                   | 将采纳最长的那一个，不足的使用fillvalue的值填充              | (p[0], q[0]), (p[1], q[1]), ...                  | `zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-` |

# 排列组合

|                            迭代器                            | 实参                 | 结果                                    |
| :----------------------------------------------------------: | :------------------- | :-------------------------------------- |
| [`product()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.product) | p, q, ... [repeat=1] | 笛卡尔积，相当于嵌套的for循环           |
| [`permutations()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.permutations) | p[, r]               | 长度r元组，所有可能的排列，无重复元素   |
| [`combinations()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.combinations) | p, r                 | 长度r元组，有序，无重复元素(**不放回**) |
| [`combinations_with_replacement()`](https://docs.python.org/zh-cn/3.8/library/itertools.html#itertools.combinations_with_replacement) | p, r                 | 长度r元组，有序，元素可重复(**放回**)   |

