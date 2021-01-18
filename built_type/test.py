import unittest


class TestType(unittest.TestCase):
    def test_logic(self):
        # 逻辑值检测

        # 通常一个对象在默认情况都视为真，除非定义了__bool__且返回False或者__len__()且返回0
        # 被定义为假值的常量: None 和 False。
        # 任何数值类型的零: 0, 0.0, 0j, Decimal(0), Fraction(0, 1) #
        # 空的序列和多项集: '', (), [], {}, set(), range(0)
        self.assertFalse(None)
        self.assertFalse(False)
        self.assertFalse(0)
        self.assertFalse(0.0)
        self.assertFalse(0j)
        self.assertFalse([])
        self.assertFalse({})

    def test_number(self):
        # 数字类型
        # Python 将 pow(0, 0) 和 0 ** 0 定义为 1，这是编程语言的普遍做法
        self.assertEqual(1, 0 ** 0)

        # 整数类型的附加方法
        self.assertEqual(len(bin(3).lstrip('-0b')), (3).bit_length())  # 返回以二进制表示一个整数所需要的位数，不包括符号位和前面的零:
        self.assertEqual(b'\x04', (4).to_bytes(1, 'little'))
        self.assertEqual(4, int.from_bytes(b'\x04', 'little', signed=False))
        self.assertTupleEqual((1, 2), 0.5.as_integer_ratio())  # 分数表达

        # 浮点数类型的附加方法
        self.assertFalse(0.3.is_integer())  # float.is_integer()如果float实例可用有限位整数表示则返回 True，否则返回 False:


if __name__ == '__main__':
    unittest.main()
