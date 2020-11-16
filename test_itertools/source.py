from itertools import *

if __name__ == '__main__':
    pass
    # for item in count(10):
    #     print(item)
    # for item in cycle('24k'):
    #     print(item)
    # for item in repeat('23', 4):
    #     print(item)

    """
    根据最短输入序列长度停止的迭代器
    """
    # for item in accumulate([1, 2, 3, 4, 5], lambda x, y: x * y):
    #     print(item)
    # for item in chain('abc', [12, 23, 45]):
    #     print(item)
    # In [6]: for item in chain.from_iterable(['abc', 'def']):
    #    ...:     print(item)
    #    ...:
    # a
    # b
    # c
    # d
    # e
    # f
    # compress压缩
    # for item in compress([1, 2, 3, 4, 5, 6], [1, 0, 1, 0]):
    #     print(item)
    # for item in dropwhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7]):
    #     print(item)
    # for item in filterfalse(lambda x: x > 3, [1, 2, 3, 4, 5, 6]):
    #     print(item)
    # In [12]: for item in groupby([1, 2, 3], lambda x: x > 2):
    #     ...:     result, iter_ = item
    #     ...:     if result:
    #     ...:         print(list(iter_))
    #     ...:
    #     ...:
    #     ...:
    #     ...:
    # [3]
    # for item in starmap(pow, [(2, 5), (3, 2), (10, 3)]):
    #     print(item)
    # 对比dropwhile
    # for item in takewhile(lambda x: x < 5, [1, 2, 3, 4, 6, 4, 1]):
    #     print(item)
    # for item in tee([1, 2, 3, 4, 5], 2): # 将会copy成两个副本的迭代器
    #     for each in item:
    #         print(each)
    # 对比zip
    # for item in zip_longest('abcd', 'xy', fillvalue='-'):
    #     print(item)

    # 排列组合
    # for item in product('abc', 'def'):
    #     print(item)
    # for item in permutations([1, 2, 3]):
    #     print(item)
    # for item in combinations([1, 2, 3], 2): # 无放回的组合
    #     print(item)
    # for item in combinations_with_replacement([1, 2, 3], 2): # 有放回的组合
    #     print(item)
