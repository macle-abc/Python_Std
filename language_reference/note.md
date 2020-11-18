# 概述
# 其他实现
- CPython
- Jython
- Python for .NET
- IronPython
- PyPy

# 词法分析
## 显示的行拼接
将多个物理行使用\拼接成一个逻辑行
```python
if 1900 < year < 2100 and 1 <= month <= 12 \
   and 1 <= day <= 31 and 0 <= hour < 24 \
   and 0 <= minute < 60 and 0 <= second < 60:   # Looks like a valid date
        return 1
```
## 关键字不可被用来作为标识符
```python
False      await      else       import     pass
None       break      except     in         raise
True       class      finally    is         return
and        continue   for        lambda     try
as         def        from       nonlocal   while
assert     del        global     not        with
async      elif       if         or         yield
```
## 字符串字面值
支持 "r" | "u" | "R" | "U" | "f" | "F" | "fr" | "Fr" | "fR" | "FR" | "rf" | "rF" | "Rf" | "RF"前缀修饰
bytes支持 "b" | "B" | "br" | "Br" | "bR" | "BR" | "rb" | "rB" | "Rb" | "RB"前缀修饰

# 数据模型
对象含有自己的编号，类型和值
编号在Cpython中就是放对象的内存地址，可以用is来比较编号
**编号和类型都是不可变得，而对象的值有些可变称之为可变对象，有些不可变称之为不可变对象**
**关于不可变类型，eg:a = 1, b = 1其id(a) id(b)可能相等，对于可变类型a = [], b = []保证id不同**
---
关于垃圾回收机制
标准只规定了可访问的对象不会被回收即可，
cpython中目前使用了(可选)延迟检测循环链接垃圾的引用计数，但是不保证会回收循环引用的情况
总之不应该依赖于垃圾回收机制***应该自己主动显示地关闭文件***

## 特殊属性

| 属性                                                         | 含义                                                         |      |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :--- |
| `__doc__`                                                    | 该函数的文档字符串，没有则为 `None`；不会被子类继承。        | 可写 |
| [`__name__`](https://docs.python.org/zh-cn/3.8/library/stdtypes.html#definition.__name__) | 类，函数，方法，描述符或生成器示例的名称。eg: Class.\_\_name\_\_   func.\_\_name\_\_ | 可写 |
| [`__qualname__`](https://docs.python.org/zh-cn/3.8/library/stdtypes.html#definition.__qualname__) | [qualified name](https://docs.python.org/zh-cn/3.8/glossary.html#term-qualified-name)。*3.3 新版功能.*   一个以点号分隔的名称，显示从模块的全局作用域到该模块中定义的**某个类、函数或方法**的“路径” | 可写 |
| `__module__`                                                 | 该函数所属模块的名称，没有则为 `None`。                      | 可写 |
| `__defaults__`                                               | 由具有默认值的参数的默认参数值组成的元组，如无任何参数具有默认值则为 `None`。 | 可写 |
| `__code__`                                                   | 表示编译后的函数体的代码对象。                               | 可写 |
| `__globals__`                                                | 对存放该函数中全局变量的字典的引用 --- 函数所属模块的全局命名空间。 | 只读 |
| [`__dict__`](https://docs.python.org/zh-cn/3.8/library/stdtypes.html#object.__dict__) | 命名空间支持的函数属性。                                     | 可写 |
| `__closure__`                                                | `__closure__ `属性返回的是一个元组对象，包含了这个闭包引用的外部变量。(`None` 或包含该函数可用变量的绑定的单元的元组。这个元组具有 `cell_contents` 属性。这可被用来获取以及设置单元的值。即获取这个闭包函数所使用了外部变量) | 只读 |
| `__annotations__`                                            | 包含参数标注的字典。字典的键是参数名，如存在返回标注则为 `'return'`。 eg: def func(args: list) | 可写 |
| `__kwdefaults__`                                             | 仅包含关键字参数默认值的字典。                               | 可写 |

**\_\_qualname\_\_的说明**

具有比name更具体的路径

```python
In [1]: def f():
   ...:     pass
   ...:

In [2]: class A:
   ...:     def f(self):
   ...:         pass
   ...:     class A:
   ...:         def f(self):pass
   ...:

In [3]: f.__name__
Out[3]: 'f'

In [4]: A.f.__name__
Out[4]: 'f'

In [5]: A.A.f.__name__
Out[5]: 'f'

In [6]: A.__name__
Out[6]: 'A'

In [7]: A.A.__name__
Out[7]: 'A'

In [8]: f.__qualname__
Out[8]: 'f'

In [9]: A.f.__qualname__
Out[9]: 'A.f'

In [10]: A.A.f.__qualname__
Out[10]: 'A.A.f'

In [11]: A.__qualname__
Out[11]: 'A'

In [12]: A.A.__qualname__
Out[12]: 'A.A'
```

---

\_\_kwdefaults\_\_的例子

```python
def foo(arg1, arg2, arg3, *args, kwarg1="FOO", kwarg2="BAR", kwarg3="BAZ"):
    pass

print(foo.__kwdefaults__)
```

## 类
类是可调用的。此种对象通常是作为“工厂”来创建自身的实例，类也可以有重载 \_\_new\_\_() 的变体类型。
调用的参数会传给\_\_new\_\_()，而且通常也会传给 \_\_init\_\_() 来初始化新的实例。

## 类实例
任意类的实例通过在所属类中定义\_\_call\_\_() 方法即能成为可调用的对象。
**属性查找**
每个类实例都有通过一个字典对象实现的独立命名空间 如果未找到类属性，而对象对应的类具有 __getattr__() 方法，则会调用该方法来满足查找要求。
实例自己的字典->有类属性->
                类属性为函数对象时，会调用该函数对象
              无类属性->
                具有\_\_getattr\_\_()方法时，会使用该方法

属性赋值和删除会更新实例的字典，但不会更新对应类的字典。如果类具有 \_\_setattr\_\_() 或 \_\_delattr\_\_() 方法，则将调用方法而不再直接更新实例的字典。

如果类实例具有某些特殊名称的方法，就可以伪装为数字、序列或映射(鸭子类型)

特殊属性: \_\_dict\_\_ 为属性字典; \_\_class\_\_ 为实例对应的类。

## 内部类型

某些由解释器内部使用的类型也被暴露给用户。它们的定义可能随未来解释器版本的更新而变化

## 特殊方法

一个类可以通过定义具有特殊名称的方法来实现由特殊语法所引发的特定操作 (例如算术运算或下标与切片)。这是 Python 实现 ***操作符重载*** 的方法

**将一个特殊方法设为 `None` 表示对应的操作不可用。例如，如果一个类将 [`__iter__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__iter__) 设为 `None`，则该类就是不可迭代的**

1. \_\_new\_\_(cls, [,...])

   **用于实例对象的创建**
   **\_\_new\_\_()是一个静态方法(因为是特例所以不需要显式地声明staticmethod)，它会将所请求实例所属的类作为第一个参数。**
   通常会使用super().\_\_new\_\_(cls, [, ...])来创建实例，然后修改这个实例并返回，对于返回的实例会进入该实例所属的\_\_init\_\_方法同时其他参数将会传递给\_\_init\_\_，如果不返回任何一个cls的实例，将不会进入任何\_\_init\_\_

   ```python
   In [58]: class A:
       ...:     def __new__(cls):
       ...:         print("new A", cls)
       ...:         return super().__new__(cls)
       ...:     def __init__(self):
       ...:         print("init A", self)
       ...:
   
   In [59]: class B(A):
       ...:     def __new__(cls):
       ...:         return A()
       ...:     def __init__(self):
       ...:         print("init B", self)
       ...:
   
   In [60]: B()
   new A <class '__main__.A'>
   init A <__main__.A object at 0x000001755B7C3850>
   In [61]: class B(A):
       ...:     def __new__(cls):
       ...:         return super().__new__(cls)
       ...:     def __init__(self):
       ...:         print("init B", self)
       ...:
   
   In [62]: B()
   new A <class '__main__.B'>
   init B <__main__.B object at 0x000001755CCD17C0>
   ```

   

2. \_\_init\_\_(self, [,...])

   返回值只能为**None**

   一个基类如果有 [`__init__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__init__) 方法，则其所派生的类如果也有 [`__init__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__init__) 方法，就必须**显式地调用它以确保实例基类部分的正确初始化**；例如: `super().__init__([args...])`.

   

3. \_\_del\_\_(self)

   `del x` 并不直接调用 `x.__del__()` --- 前者会将 `x` 的引用计数减一，而后者仅会在 `x` 的引用计数变为零时被调用。

4. \_\_repr\_\_(self)

   此方法通常被用于调试，因此确保其表示的内容包含丰富信息且无歧义是很重要的。

   `个人推荐写法<classname object other info>`

5. \_\_str\_\_(self)

   内置类型 [`object`](https://docs.python.org/zh-cn/3.8/library/functions.html#object) 所定义的默认实现会调用 [`object.__repr__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__repr__)。
   
6. `object.__lt__`(*self*, *other*)

   `object.__le__`(*self*, *other*)

   `object.__eq__`(*self*, *other*)

   `object.__ne__`(*self*, *other*)

   `object.__gt__`(*self*, *other*)

   `object.__ge__`(*self*, *other*)

   比较运算符
   
   在默认情况下，`object` 通过使用 `is` 来实现 [`__eq__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__eq__)，并在比较结果为假值时返回 `NotImplemented`: `True if x is y else NotImplemented`
   
7. \_\_bool_\_(self)

   应该返回 `False` 或 `True`。如果未定义此方法，则会查找并调用 [`__len__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__len__) 并在其返回非零值时视对象的逻辑值为真。如果一个类既未定义 [`__len__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__len__) 也未定义 [`__bool__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__bool__) 则视其所有实例的逻辑值为真。

8. \_\_hash\_\_(self)

   **[`__hash__()`](https://docs.python.org/zh-cn/3.8/reference/datamodel.html#object.__hash__) 应该返回一个整数。**

   常见做法：

   ```python
   def __hash__(self):
       return hash((self.name, self.nick, self.color))
   ```

   **将所有属性设置为元组，然后进行hash**

   hash应该是不可变对象

   **\_\_eq\_\_和\_\_hash\_\_应该成对出现，否则只定义了\_\_eq\_\_将会导致\_\_hash\_\_ = None**

9. \_\_bytes\_\_(self) 
   \_\_format\_\_(self, format_spec)

### 属性访问

`x.name` 的使用、赋值或删除

1.\_\_getattribute\_\_(self, name)
    此方法会无条件地被调用以实现对类实例属性的访问。如果类还定义了`__getattr__()`则后者不会被调用，除非`__getattribute__()`显式地调用它或是引发了`AttributeError`
    **尤其注意为了避免递归，应该调用基类方法去访问**

~~~python
```python
In [11]: class A:
...:     a = 1
...:

In [12]: class B(A):
    ...:     b = 2
    ...:     def __getattribute__(self, name):
    ...:         return super().__getattribute__(name)
    ...:

In [13]: b = B()

In [14]: b.a
Out[14]: 1

In [15]: b.b
Out[15]: 2

In [16]: b.c
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-16-4592cda7d891> in <module>
----> 1 b.c

<ipython-input-12-c64feac76a00> in __getattribute__(self, name)
      2     b = 2
      3     def __getattribute__(self, name):
----> 4         return super().__getattribute__(name)
      5

AttributeError: 'B' object has no attribute 'c'
```
~~~

2. \_\_getattr\_\_(self, name)
    当因引发AttributeError时被调用，应返回找到的值或者引发AttributeError(不会引发递归)
    pass

3. \_\_setattr\_\_(self, name, value)
    被赋值时调用会取代默认行为**将name:value保存到实例字典里面**
    应该调用基类的方法
    
4. \_\_delattr\_\_(self, name)
    用途**仅在del obj.name对于该对象有意义的时候才会被实现** 
5. \_\_dir\_\_(self)
    此方法会在对相应对象调用 dir() 时被调用。返回值必须为一个序列(可迭代对象), dir会把这个转化为list再排序


### 属性描述符
当一个类的属性为一个类(定义了以下方法)的实例时才会起作用
1. \_\_get\_\_(self, instance, owner=None)
    此方法应当返回计算得到的属性值或是引发 AttributeError 异常。
    ```python
    In [9]: class ADescriptor:
    ...:     def __get__(self, instance, owner=None):
    ...:         '''
    ...:         @params self:为ADescriptor的实例
    ...:         @params instance:为属性描述符的拥有者的实例
    ...:         @params owner:为拥有者这个类
    ...:         return: 属性
    ...:         raise: AttributeError
    ...:         '''
    ...:         print(f"self:{self}, instance:{instance}, owner:{owner}")
    ...:         return "descriptor"
    ...:

    In [10]: class A:
        ...:     a = ADescriptor()
        ...:     def __init__(self, v):
        ...:         self.v = v
        ...: 
    In [12]: a = A(2)

    In [13]: a.a
    self:<__main__.ADescriptor object at 0x000002C7391080D0>, instance:<__main__.A object at 0x000002C739108220>, owner:<class '__main__.A'>
    Out[13]: 'descriptor'

    In [14]: a.v
    Out[14]: 2
   ```
   
2. \_\_set\_\_(self, instance, value)
    **设置\_\_set\_\_或者\_\_delete\_\_会将描述符变成数据描述符**

3. \_\_delete\_\_(self, instance)
   
4. \_\_set\_name\_\_(self, owner, name)
    在所有者类owner创建时被调用(owner被type创建时，隐式调用)。描述器会被赋值为name。
    ```python
    In [41]: class ADescriptor:
        ...:      def __set_name__(self, owner, name):
        ...:          print(self, owner, name)

    In [42]: class A:
        ...:     a = ADescriptor()
        ...:
    <__main__.ADescriptor object at 0x000002C7393A9130> <class '__main__.A'> a
    ```
    
### 理解描述符
其属性访问已被描述器协议中的方法所重载，包括\_\_get\_\_(), \_\_set\_\_() 和 \_\_delete\_\_()。如果一个对象定义了以上方法中的任意一个，它就被称为描述器。
默认的属性查找:
```
a.x == a.__dict__['x'] -> type(a).__dict__['x'] 一直到基类(**不包括元类**)
```
---
描述器发起调用的开始点是a.x。参数的组合方式依a而定:
- 直接调用
最简单但最不常见的调用方式是用户代码直接发起调用一个描述器方法: x.\_\_get\_\_(a)。

- 实例绑定
    如果x绑定到一个对象实例，a.x 会被转换为调用: type(a).\_\_dict__\['x'\].\_\_get\_\_(a, type(a))。

- 类绑定
    如果x绑定到一个类，A.x 会被转换为调用: A.\_\_dict_\_\['x'\].\_\_get\_\_(None, A)。

- 超绑定
    如果a是super的一个实例，则super(B, obj).m()**(即a = super(B, obj)即a是B的父类)**
    ```
    会在 obj.__class__.__mro__ 中搜索 B 的直接上级基类 A 然后通过以下调用发起调用描述器: A.__dict__['m'].__get__(obj, obj.__class__)。  
    ```
---
如果一个描述符没有定义\_\_get\_\_()，则访问属性会返回描述器对象自身，除非对象的实例字典中有相应属性值。
```python
In [85]: class D:
    ...:     def __get__(self, instance, owner=None): # 若没定义该方法
    ...:         print("get", self, instance, owner)
    ...:
In [86]: class A:
    ...:     d = D()
    ...:

In [87]: A.d
get <__main__.D object at 0x000001F2B1378700> None <class '__main__.A'>

In [88]: A().d
get <__main__.D object at 0x000001F2B1378700> <__main__.A object at 0x000001F2B25E5370> <class '__main__.A'>
In [95]: class D:
    ...:     def __set_name__(self, instance, name):
    ...:         print(self, instance, name)
    ...:

In [96]: class A:
    ...:     d = D()
    ...:
<__main__.D object at 0x000001F2B26F5490> <class '__main__.A'> d

In [97]: A.d
Out[97]: <__main__.D at 0x1f2b26f5490>

In [98]: A().d
Out[98]: <__main__.D at 0x1f2b26f5490>
```
---

如果描述器定义了\_\_set\_\_() 和/或 \_\_delete\_\_()，则它是一个数据描述器；
如果以上两个都未定义，则它是一个非数据描述器。

---

通常，数据描述器会同时定义\_\_get\_\_() 和 \_\_set\_\_()
而非数据描述器只有\_\_get\_\_() 方法
其中a为A的实例
定义了\_\_set\_\_() 和 \_\_get\_\_() 的数据描述器总是会[^重载],实例字典中的定义(即a.x = 2的时候会调用\_\_set\_\_)。

[^重载]:之所以叫重载,因为访问其他非描述符的属性时是按照正常模式去访问的

```python
In [101]: class D:
     ...:     def __set__(self, instance, value):
     ...:         print(self, instance, value)
     ...:

In [102]: class A:
     ...:     d = D()
     ...:

In [103]: a = A()
In [106]: a.d = 2
<__main__.D object at 0x000001F2B13174F0> <__main__.A object at 0x000001F2B2E9F9A0> 2

In [107]: a.d = 3
<__main__.D object at 0x000001F2B13174F0> <__main__.A object at 0x000001F2B2E9F9A0> 3
```

与之相对的，非数据描述器可被实例所重载(即a.x = 2的时候会真的修改x的类型为int)

```python 
In [112]: class D:
     ...:     def __get__(self, instance, owner):
     ...:         print(self, instance, owner)
     ...:

In [113]: class A:
     ...:     d = D()
     ...:

In [114]: a = A()

In [115]: a.d
<__main__.D object at 0x000001F2B133C4F0> <__main__.A object at 0x000001F2B1437280> <class '__main__.A'>

In [116]: a.d = 3

In [117]: a.d
Out[117]: 3
```

### 对于数据描述符和非数据描述符的两个例子
1. 数据描述符property
    ```python
    In [7]: class Test:
       ...:     @property
       ...:     def x(self):
       ...:         print("get x")
       ...:         return self._x
       ...:     @x.setter
       ...:     def x(self, value):
       ...:         print("set x")
       ...:         self._x = value
       ...:     @x.deleter
       ...:     def x(self):
       ...:         del self._x
       ...:

    In [8]: t = Test()
    In [10]: t.x = 3
    set x

    In [11]: t.x
    get x
    Out[11]: 3
    ```
   
2. 非数据描述符staticmethod / classmethod
    ```python
    In [14]: class T:
        ...:     @staticmethod
        ...:     def func(args):
        ...:         print(args)
        ...:

    In [15]: t = T()

    In [16]: t.func(2)
    2

    In [17]: t.func = 3

    In [18]: t.func
    Out[18]: 3
    ```

