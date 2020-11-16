# 基础使用
默认支持-h, --help可选参数
```python
import argparse
parse = argparse.ArgumentParser()
print(parse.parse_args())
```
1. 位置参数
    ```python
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("echo", help="help string", type=str)  # 位置参数，设置帮助提示, 设置该参数的类型，默认是str
    args = parse.parse_args()
    print(args.echo) # 将会自动增加该属性
    ```

2. 可选参数
    1. 长选项
        ```python
        import argparse
        parser = argparse.ArgumentParser()
        # 长选项, 默认会产生同名的位置参数eg: --verbosity string 这里的string即为verbosity的值
        # 当关键字参数action:
        #     "store_true":表示verbosity的值为True Or False 且无需额外的string作为verbosity的值，当有该选项时即为True
        parser.add_argument("--verbosity", help="increase output verbosity")
        args = parser.parse_args()
        if args.verbosity:
            print("verbosity turned on")
            print(args.verbosity)
        ```
    2. 短选项
        ```python
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="increase output verbosity",
                            action="store_true")
        args = parser.parse_args()
        if args.verbose:
            print("verbosity turned on")
        ```

## 限制参数的取值范围
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity", choices=list(range(3))) # 范围即为可迭代对象的每一个元素
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

## 根据可选参数出现次数来决定
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
# action="count"时，将会统计v出现的次数来转换为int值
# eg: --verbosity --verbosity -vv 表示verbosity的值为4
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

## 为可选参数设置默认值
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
# 默认值,应该结合action使用
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

## 互斥的选项
add_mutually_exclusive_group()。 它允许我们指定彼此相互冲突的选项

```python
import argparse
# 设置程序描述
parser = argparse.ArgumentParser(description="calculate X to the power of Y")
# 创建互斥组
group = parser.add_mutually_exclusive_group()
# 互斥组添加参数
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
```

# API用法
## ArgumentParse对象
```python
class ArgumentParser(prog=None, usage=None, description=None, 
    epilog=None, parents=[], 
    formatter_class=argparse.HelpFormatter, 
    prefix_chars='-', fromfile_prefix_chars=None, 
    argument_default=None, conflict_handler='error', 
    add_help=True, allow_abbrev=True):
    pass
```
**应该全部使用关键字参数来调用**

1. prog
   
    程序的名称（默认值：sys.argv[0]）
    对于该prog，在比如help关键字参数中可以使用%(prog)s来引用prog
    eg:
    
    ```python
    parser.add_argument('--foo', help='foo of the %(prog)s program')
    ```
    
2. usage

    描述程序用途的字符串（默认值：从添加到解析器的参数生成）

3. description

    在参数帮助文档之前显示的文本（默认值：无）

4. epilog

    在参数帮助文档之后显示的文本（默认值：无）

5. parents

    一个 ArgumentParser 对象的列表，用于给子解释器复用父对象的配置
    **需要注意的是由于-h选项默认是True，会存在父子解释器两个-h的情况将会抛出错误**
    **因此在初始化父类解释器的时候应该使用add_help=False来阻止这种行为**

6. formatter_class

    用于自定义帮助文档输出格式的类
    推荐ArgumentDefaultsHelpFormatter 自动添加默认的值的信息到每一个帮助信息的参数中

    ```python
    In [13]: parser = argparse.ArgumentParser(
    ...:     prog='PROG',
    ...:     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ...: parser.add_argument('--foo', type=int, default=42, help='FOO!')
    ...: parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
    ...: parser.print_help()
    ...:
    usage: PROG [-h] [--foo FOO] [bar [bar ...]]
    
    positional arguments:
      bar         BAR! (default: [1, 2, 3])
    
    optional arguments:
      -h, --help  show this help message and exit
      --foo FOO   FOO! (default: 42)  
    ```

7. prefix_chars

    可选参数的前缀字符集合（默认值： '-'）

8. fromfile_prefix_chars

    当需要从文件中读取其他参数时，用于标识文件名的前缀字符集合（默认值： None）
    ```python
    >>> with open('args.txt', 'w') as fp:
    ...     fp.write('-f\nbar')
    >>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    >>> parser.add_argument('-f')
    >>> parser.parse_args(['-f', 'foo', '@args.txt'])  # 解析参数时看到@args.txt将会视为从该文件读取参数
    # 从文件读取的参数在默认情况下必须一个一行
    # 同时参数会update为文件中的参数
    Namespace(f='bar')
    ```
    
9. argument_default

    参数的全局默认值（默认值： None）

10. conflict_handler

    解决冲突选项的策略（通常是不必要的）

11. add_help

     为解析器添加一个 -h/--help 选项（默认值： True）

12. allow_abbrev

     如果缩写是无歧义的(eg: \-\-foobar \-\-foonley那么将会出现歧义)，则允许缩写长选项 （默认值：True）

## add_argument()方法
ArgumentParser.add_argument(name or flags...\[, action\]]\[, nargs\]\[, const\]\[, default\]\[, type\]\[, choices\]\[, required\]\[, help\]\[, metavar\]\[, dest\])
定义单个的命令行参数应当如何解析。每个形参都在下面有它自己更多的描述，长话短说有：

1. name or flags
    一个命名或者一个选项字符串的列表，
    例如 foo 或 -f, --foo。
    eg:
    
    ```python
    parse.add_argument('bar')
    parse.add_argument('-f', '-foo')
    ```
    
2. action
    当参数在命令行中出现时使用的动作基本类型。
    
    1. 'store' (默认)
        存储参数的值
        
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo')
        >>> parser.parse_args('--foo 1'.split())
        Namespace(foo='1') 
        ```
    2. 'store\_const'
        存储到const参数指定的值
        
        'store\_true'
        ---
        'store\_false'是这个选项的特殊情况
        ---
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', action='store_const', const=42)
        >>> parser.parse_args(['--foo'])
        Namespace(foo=42)
        ```
    3. 存储到列表中
        'append' (该配置需要用户输入值)
        
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', action='append')
        >>> parser.parse_args('--foo 1 --foo 2'.split())
        Namespace(foo=['1', '2'])
        ```
        ---
        'append_const' (该配置将采用const的值来添加到list中而不需要用户输入eg:--foo FOO)
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
        >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
        >>> parser.parse_args('--str --int'.split())
        Namespace(types=[<class 'str'>, <class 'int'>])
        ```
    4. 统计关键字参数出现的次数
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--verbose', '-v', action='count', default=0)
        >>> parser.parse_args(['-vvv'])
        Namespace(verbose=3)
        ```
    
3. nargs
    命令行参数应当消耗的数目。
    **若没有指定nargs则消耗的参数由action来决定**
    1. N(一个整数)命令行中的N个参数会被聚集到一个列表中
        **尤其是当N=1的时候**
        ```python
        In [6]: parser = argparse.ArgumentParser()
           ...: parser.add_argument('--foo', nargs=2)
           ...: parser.add_argument('bar', nargs=1)
           ...: parser.parse_args('c --foo a b'.split())
           ...: #Namespace(bar=['c'], foo=['a', 'b'])
        Out[6]: Namespace(bar=['c'], foo=['a', 'b'])

        In [7]: parser = argparse.ArgumentParser()
           ...: parser.add_argument('--foo', nargs=2)
           ...: parser.add_argument('bar') #, nargs=1)
           ...: parser.parse_args('c --foo a b'.split())
           ...: #Namespace(bar='c', foo=['a', 'b'])
        Out[7]: Namespace(bar='c', foo=['a', 'b'])
        ```
    2. '?'，类似正则表达式的?表示可有可无，当没有该参数时将采纳default的值，但是如果该参数是一个选项的话而且没有指定后面的参数(eg:-foo \[FOO\]没有传入)，那么将会采纳const的值而非default的值 
        ```python
        parser = argparse.ArgumentParser()
        parser.add_argument('--foo', nargs='?', const='c', default='d')
        parser.add_argument('bar', nargs='?', default='d')
        parser.parse_args(['XX', '--foo', 'YY'])
        >>> Namespace(bar='XX', foo='YY')
        parser.parse_args(['XX', '--foo'])
        >>> Namespace(bar='XX', foo='c')
        parser.parse_args([])
        >>> Namespace(bar='d', foo='d') 
        ```  
        **通常用于配置读写默认文件**
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
        ...                     default=sys.stdin)
        >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
        ...                     default=sys.stdout)
        >>> parser.parse_args(['input.txt', 'output.txt'])
        Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
                  outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
        >>> parser.parse_args([])
        Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
                  outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)
        ```
    3. '*' 所有当前命令行参数被聚集到一个列表中和'+'基本类似，但是'+'要求至少有一个
        **一般用于多个选项**
        **而+一般用于位置参数eg:python sum.py 1 2 3 4** 
        ```python
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', nargs='*')
        >>> parser.add_argument('--bar', nargs='*')
        >>> parser.add_argument('baz', nargs='*')
        >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
        Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])
        ```
        ---
        ```python
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('foo', nargs='+')
        >>> parser.parse_args(['a', 'b'])
        Namespace(foo=['a', 'b'])
        >>> parser.parse_args([])
        usage: PROG [-h] foo [foo ...]
        PROG: error: the following arguments are required: foo 
        ```
    4. argparse.REMAINDER 
        截断当前及其后面的参数组合一个list，一般用于给其他命令传递参数(eg:python cmd.py ls 1.txt 2.txt)
        ```python
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('--foo')
        >>> parser.add_argument('command')
        >>> parser.add_argument('args', nargs=argparse.REMAINDER)
        >>> print(parser.parse_args('--foo B cmd --arg1 XX ZZ'.split()))
        Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')
        ```

4. const
    被一些 action 和 nargs 选择所需求的常数。
    action:'store_const' 'append_const'
    nargs:'?'

5. default
    当参数未在命令行中出现时使用的值。
    ```python
    # 提供 default=argparse.SUPPRESS 导致命令行参数未出现时没有属性被添加:
    >>> parser = argparse.ArgumentParser()
    # suppress抑制
    >>> parser.add_argument('--foo', default=argparse.SUPPRESS)
    >>> parser.parse_args([])
    Namespace()
    >>> parser.parse_args(['--foo', '1'])
    Namespace(foo='1')
    ```

6. type
    命令行参数应当被转换成的类型。
    **可接受任意可调用对象，该对象应传入单个字符串参数并返回转换后的值:**
    **对于文件操作，argparse提供了文件工厂类argparse.FileType(), 以便更多的自定义，来弥补只能使用open作为参数的缺陷**
    ```python
    def perfect_square(string):
        value = int(string)
        sqrt = math.sqrt(value)
        if sqrt != int(sqrt):
            msg = "%r is not a perfect square" % string
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('foo', type=perfect_square)
    parser.parse_args(['9'])

    parser.parse_args(['7'])
    ``` 

7. choices
    可用的参数的容器。
    **容器包含的内容会在执行任意type转换之后被检查，因此choices容器中对象的类型应当与指定的type相匹配**

8. required
    此命令行选项是否可省略 （仅选项可用）。
    **必需的选项通常被认为是不适宜的，因为options都是可选的，因此在可能的情况下应当避免使用它们。**

9. help
    一个此选项作用的简单描述。
    可以引用其他关键字参数的配置eg:help='%(prog)s %(default)s'

10. metavar
    在使用方法消息中使用的参数值示例。

11. dest
    被添加到 parse\_args() 所返回对象上的属性名。

12. version
    ```python
    >>> import argparse
    >>> parser = argparse.ArgumentParser(prog='PROG')
    >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    >>> parser.parse_args(['--version'])
    PROG 2.0
    ```
    
    