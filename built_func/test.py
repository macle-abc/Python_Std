import unittest


class TestBuilt(unittest.TestCase):
    # # 动态编译执行
    # # compile()
    # # eval()
    # # exec()

    # 会对每一个test开头的方法都调用
    # def setUp(self) -> None:
    #     print("进入测试")
    #
    # def tearDown(self) -> None:
    #     print("退出")

    def test_a(self):
        self.assertEqual(5, abs(3 + 4j))  # 如果是负数则返回它的模
        self.assertTrue(all([1, 2, 3]))  # 如果都为真（或者iterable为None）则返回True
        self.assertTrue(all([]))
        self.assertTrue(any([1, 2, 0]))  # 如果任一元素为真则返回True，当iterable为None时返回False
        self.assertFalse(any([]))
        self.assertEqual("'中'", repr('中'))  # 基本等价repr，除了对于非ASCII字符的会以\x, \u和\U来转义
        self.assertTrue('\u4e2d', ascii('中'))

    def test_b(self):
        self.assertEqual('0b11', bin(3))  # 返回带有前缀'0b'的二进制字符串，可以定义__index__()方法返回整数
        self.assertEqual('11', f"{3:b}")
        self.assertFalse(bool())  # 只有False和True的两个实例，为int的子类
        self.assertTrue(issubclass(bool, int))
        self.assertEqual(b'1', bytes('1', 'utf-8'))  # bytearray的不可变版本，同时允许使用字面值创建

    def test_c(self):
        self.assertTrue(callable(lambda x: x))  # 如果obj是可调用的则返回True，可以定义__call__()
        self.assertEqual('a', chr(97))  # 返回unicode编码为97的字符串形式，范围是0-0x10ffff
        # @classmethod 把一个方法封装成类方法
        self.assertEqual(3 + 4j, complex(3, 4))  # 复数

    def test_d(self):
        self.assertRaises(AttributeError, delattr, int(), 'real')  # 等价于del int().real
        self.assertDictEqual({"a": 1, "b": 2}, dict(a=1, b=2))
        # dir() 默认打印本地作用域的名称列表
        # 默认的 dir() 机制对不同类型的对象行为不同，它会试图返回最相关而不是最全的信息：
        # 如果对象是模块对象，则列表包含模块的属性名称。
        # 如果对象是类型或类对象，则列表包含它们的属性名称，并且递归查找所有基类的属性。
        # 否则，列表包含对象的属性名称，它的类属性名称，并且递归查找它的类的所有基类的属性。
        self.assertTupleEqual((5 // 3, 5 % 3), divmod(5, 3), "show this message when not equal")
        self.assertListEqual([(1, 'a'), (2, 'b'), (3, 'c')], list(enumerate("abc", start=1)))  # start决定枚举值的起始值

    def test_f(self):
        self.assertListEqual([1, 2],
                             list(filter(lambda x: True if x < 3 else False, [1, 2, 3, 4])))  # 返回一个满足lambda为True的生成器
        self.assertListEqual([1, 2, 3],
                             list(filter(None, [1, 2, 3, 0, False])))
        # 当filter的第一个参数为None时则会假设它是一个身份函数，即 iterable 中所有返回假的元素会被移除。
        self.assertFalse(float('-inf') > 3)
        # float('nan'), float('-inf'), float('inf'))  # 非数字和无穷大
        self.assertSetEqual({1, 2, 3, 4}, frozenset([1, 2, 3]).union([3, 4]))  # set的不可变版本

    def test_g(self):
        self.assertEqual("23".encode, getattr("23", "encode"))
        # globals()  # 总是返回它当前所在的模块的全局字典，在函数或者方法中，是返回定义它的模块全局字典而非调用它的模块

    def test_h(self):
        self.assertEqual('0xff', hex(255))
        self.assertEqual('ff', f"{255:x}")  # 类似bin

    def test_i(self):
        # id(object)返回对象的“标识值”。该值是一个整数，在此对象的生命周期中保证是唯一且恒定的。两个生命期不重叠的对象可能具有相同的 id() 值。
        # CPython implementation detail: This is the address of the object in memory.
        # self.assertEqual("234", input())  # 输入234
        self.assertEqual(0xff, int('255'))
        self.assertTrue(isinstance(123, int))
        from collections import OrderedDict
        self.assertTrue(issubclass(OrderedDict, dict))
        # iter()
        # Get an iterator from an object.
        # In the first form, the argument must supply its own iterator, or be a sequence.
        # In the second form, the callable is called until it returns the sentinel.
        # eg: 构建每次读取64byte的块
        # from functools import partial
        # with open('mydata.db', 'rb') as f:
        #     for block in iter(partial(f.read, 64), b''):  # 不断不带参数地调用partial()，直到返回b''
        #         process_block(block)
        self.assertEqual(3, len('123'))
        self.assertListEqual([], list())
        # locals()
        # 更新并返回表示当前本地符号表的字典。
        # 在函数代码块但不是类代码块中调用 locals() 时将返回自由变量。
        # 在模块层级上，locals() 和 globals() 是同一个字典。

    def test_m(self):
        self.assertTupleEqual((1, 4, 9), tuple(map(lambda x, y: x * y, [1, 2, 3], [1, 2, 3])))
        self.assertEqual(100, int(max(map(str, [1, 2, 40, 50, 100]), key=len)))
        # class memoryview(obj) 返回由给定实参创建的“内存视图”对象。 类似c语言指针
        self.assertEqual(1, int(min(map(str, [1, 2, 40, 50, 100]), key=len)))

    # next(iterator[, default])
    # Return the next item from the iterator. If default is given and the iterator
    # is exhausted, it is returned instead of raising StopIteration.

    def test_o(self):
        # object() 没有__dict__，是所有类的基类
        self.assertEqual('0o10', oct(8))
        self.assertEqual('10', f"{8:o}")
        # open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
        # 'r'        # 读取（默认）
        # 'w'        # 写入，并先截断文件
        # 'x'        # 排它性创建，如果文件已存在则失败
        # 'a'        # 写入，如果文件存在则在末尾追加
        # 'b'        # 二进制模式
        # 't'        # 文本模式（默认）
        # '+'        # 打开用于更新（读取与写入）
        self.assertEqual(97, ord('a'))  # ord(c)对表示单个 Unicode 字符的字符串，返回代表它 Unicode 码点的整数

    def test_p(self):
        # pow(base, exp[, mod])返回 base 的 exp 次幂；
        # 如果 mod 存在，则返回 base 的 exp 次幂对 mod 取余（比 pow(base, exp) % mod 更高效）。 ->大数取余
        # 两参数形式 pow(base, exp) 等价于乘方运算符: base**exp。
        self.assertEqual(2 ** 3, pow(2, 3))
        # print(*objects, sep=' ', end='n', file=sys.stdout, flush=False)
        # class property(fget=None, fset=None, fdel=None, doc=None) 返回 property 属性。 可使用装饰器的语法

    def test_r(self):
        # class range(stop)class range(start, stop[, step])虽然被称为函数，但 range 实际上是一个不可变的序列类型，
        # repr() 在其他情况下表示形式会是一个括在尖括号中的字符串，其中包含对象类型的名称与通常包括对象名称和地址的附加信息。 类可以通过定义 __repr__() 方法来控制此函数为它的实例所返回的内容。
        self.assertListEqual([3, 2, 1], list(reversed(range(1, 4))))
        # round(number[, ndigits])返回 number 舍入到小数点后 ndigits 位精度的值。 如果 ndigits 被省略或为 None，则返回最接近输入值的整数。
        self.assertEqual(5.5, round(5.48, 1))
        self.assertEqual(6, round(5.78))

    def test_s(self):
        # set()

        # setattr(obj, name, value)

        # class slice(stop)# class slice(start, stop[, step])
        # 返回一个表示由 range(start, stop, step) 所指定索引集的 slice 对象。 其中 start 和 step 参数默认为 None，具有start, stop, step这三个只读属性

        # sorted(iterable, *, key=None, reverse=False)
        # 根据 iterable 中的项返回一个新的已排序列表。
        # 具有两个可选参数，它们都必须指定为关键字参数。
        # key 指定带有单个参数的函数，用于从 iterable 的每个元素中提取用于比较的键 (例如 key=str.lower)。 默认值为 None (直接比较元素)。
        # reverse 为一个布尔值。 如果设为 True，则每个列表元素将按反向顺序比较进行排序(默认升序排序)
        # 并且是稳定的排序算法(相同元素的位置不会发生修改)
        self.assertListEqual([[4, 5], [1], [2], [3]], sorted([[1], [2], [3], [4, 5]], key=len, reverse=True))

        # @staticmethod
        # 将方法转换为静态方法。

        # class str(object='')
        # class str(object=b'', encoding='utf-8', errors='strict')
        # 返回一个 str 版本的 object
        self.assertEqual(10, sum([1, 2, 3, 4]))  # iterable通常为数字

        # super([type[, object-or-type]])mro算法，根据当前的__mro寻找到当前对象的下一个

    def test_t(self):
        self.assertTupleEqual((), tuple())  # 不可变序列

        # type(object) -> the object's type
        # type(name, bases, dict) -> a new type

    # vars([object])
    # 返回模块、类、实例或任何其它具有 __dict__ 属性的对象的 __dict__ 属性。

    def test_z(self):
        self.assertListEqual([(1, 2, 3)], list(zip([1], [2], [3])))  # 创建一个聚合了来自每个可迭代对象中的元素的迭代器。
        # 会选择iterables中最短的组合， itertools.zip_longest()则相反


if __name__ == '__main__':
    unittest.main()
