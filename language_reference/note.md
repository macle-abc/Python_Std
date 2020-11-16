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
    **尤其注意为了避免递归**

    ```python
    In [43]: class B(A):
        ...:     b = 3
        ...:     def __getattribute__(self, name):
        ...:         print("log name")
        ...:         try:
        ...:             return object.__getattribute__(self, name)
        ...:         except AttributeError:
        ...:             return "other attribute"
        ...:
    In [44]: B().a
    log name
    Out[44]: 2

    In [45]: B().b
    log name
    Out[45]: 3

    In [46]: B().c
    log name
    Out[46]: 'other attribute'
        ```

2. \_\_getattr\_\_(self, name)
    pass
