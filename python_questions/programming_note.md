1. 为什么在具有不同值的循环中定义的lambdas都返回相同的结果？
    ```python
    In [22]: squares = []
    In [23]: for x in range(5):
        ...:     squares.append(lambda: x**2)
        ...:
    In [24]: squares[1]()
    Out[24]: 16
    In [25]: squares[2]()
    Out[25]: 16 
    ```
    **正确写法**
    ```python
    In [26]: squares = []
    In [27]: for x in range(5):
        ...:     squares.append(lambda n=x: n**2)
        ...:
        ...:
    In [28]: squares[1]()
    Out[28]: 1
    In [29]: squares[2]()
    Out[29]: 4
    In [30]: squares[3]()
    Out[30]: 9
    ```
 
  
2. 模块导入顺序推荐做法
    1. 标准库
    2. 第三方库
    3. 本地开发的自定义库
    
3. 关于默认值的问题
    按照定义，不可变对象例如数字、字符串、元组和 None 因为不可变所以是安全的。 对可变对象例如字典、列表和类实例的改变则可能造成迷惑。
    ```python
    def foo(mydict = {}):
        pass # 不推荐写法，因为默认值在函数定义时就会一次性创建好
    ```
   因此对于该种问题**应该不使用可变对象作为默认值**而应该使用None来作为默认值
   eg:
   ```python
   def foo(mydict = None):
       if mydict is None:
           mydict = {} 
   ```
   
4. 修改x列表，y也被修改?
    ```python
    In [46]: a = [1, 2, 3]
    In [47]: b = a
    In [48]: a[0] = 4
    In [49]: a
    Out[49]: [4, 2, 3]
    In [50]: b
    Out[50]: [4, 2, 3]
    ```
    如果我们有一个可变对象 (list, dict, set 等等)，我们可以使用某些特定的操作来改变它，所有指向它的变量都会显示它的改变。
    如果我们有一个不可变对象 (str, int, tuple 等等)，所有指向它的变量都将显示相同样的值，但凡是会改变这个值的操作将总是返回一个新对象。

5. 创建高阶函数
    1. 使用嵌套定义的方式
    2. 使用可调用对象(重载\_\_call\_\_)
   
6. 复制对象
    copy.copy() # 浅拷贝
    copy.deepcopy()
    ```python
    In [57]: import copy
    In [58]: a = [1, 2, [3]]
    In [59]: b = copy.copy(a)
    In [60]: c = copy.deepcopy(a)
    In [64]: a[2].append('fw')
    In [65]: a
    Out[65]: [1, 2, [3, 'fw']]
    In [66]: b
    Out[66]: [1, 2, [3, 'fw']]
    In [67]: c
    Out[67]: [1, 2, [3]]
    ```

7. 函数的参数列表的/和\*的含义
    表明在/之前的形参都必须是位置参数
    表明在\*之后的形参都必须是关键字参数
    ```python
    In [83]: divmod?
    Signature: divmod(x, y, /)
    Docstring: Return the tuple (x//y, x%y).  Invariant: div*y + mod == x.
    Type:      builtin_function_or_method

    In [84]: divmod(2, 3)
    Out[84]: (0, 2)

    In [85]: divmod(x=2, y=3)
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-85-d9e15dc18919> in <module>
    ----> 1 divmod(x=2, y=3)

    TypeError: divmod() takes no keyword arguments
    ```
    ---
    ```python
    In [88]: def func(*, a, b):
        ...:     return a + b
        ...:

    In [89]: func(2, 3)
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-89-2b92b04f16f8> in <module>
    ----> 1 func(2, 3)

    TypeError: func() takes 0 positional arguments but 2 were given

    In [90]: func(b=2, a=3)
    Out[90]: 5
    ```
   
8. 将多个字符串连接在一起的最有效的方法是?
    **要连接多个str对象，通常推荐的用法是将它们放入一个列表中并在结尾处调用str.join()**

9. 什么是委托
    委托是一种面向对象的技巧（也称为设计模式）。 假设您有一个对象 x 并且想要改变其中一个方法的行为。 您可以创建一个新类，它提供您感兴趣的方法的新实现，并将所有其他方法委托给 x 的相应方法
    尽管可以使用继承来达到同样的效果
    eg:
    ```python
    class UpperOut:
        def __init__(self, outfile):
            self._outfile = outfile

        def write(self, s):
            # 仅仅覆盖该方法
            self._outfile.write(s.upper())

        def __getattr__(self, name):
            # 其他的属性调用将委托给self._outfile去获取
            return getattr(self._outfile, name)
    ```
    **大多数情况可能需要定义\_\_setattr\_\_()方法**
    
10: 循环导入
    ```python
    foo.py:
    from bar import bar_var
    foo_var = 1
    bar.py:
    from foo import foo_var
    bar_var = 2
    ```
    1. 首先导入foo
    2. 创建用于foo的空全局变量
    3. foo被编译开始执行
    4. foo导入bar
    5. 创建用于bar的空全局变量
    6. bar被编译开始执行
    7. bar导入foo(空操作，因为已经导入了foo的模块)
    8. bar.foo_var = foo.foo_var (失败，因为foo还没开始解释，foo的全局符号字典为空)
   