import unittest


class TestStringMethods(unittest.TestCase):  # 创建测试用例
    # 需要测试的方法以test开头
    # 没有使用assert语句是为了让测试运行者能聚合所有的测试结果并产生结果报告
    def setUp(self) -> None:
        print("初始化内容!")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)

    def tearDown(self) -> None:
        print("清理内容!")


if __name__ == '__main__':
    unittest.main()
    # python file.py
    # python file.py -v 详细信息
