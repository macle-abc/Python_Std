| 字符 |   字节顺序    |   大小   | 对齐方式 |
| :--: | :-----------: | :------: | :------: |
| `@`  |   按原字节    | 按原字节 | 按原字节 |
| `=`  |   按原字节    |   标准   |    无    |
| `<`  |     小端      |   标准   |    无    |
| `>`  |     大端      |   标准   |    无    |
| `!`  | 网络（=大端） |   标准   |    无    |


| 格式 |        C 类型        |    Python 类型    | 标准大小 |   注释   |
| :--: | :------------------: | :---------------: | :------: | :------: |
| `x`  |       填充字节       |        无         |          |          |
| `c`  |        `char`        | 长度为 1 的字节串 |    1     |          |
| `b`  |    `signed char`     |       整数        |    1     | (1), (2) |
| `B`  |   `unsigned char`    |       整数        |    1     |   (2)    |
| `?`  |       `_Bool`        |       bool        |    1     |   (1)    |
| `h`  |       `short`        |       整数        |    2     |   (2)    |
| `H`  |   `unsigned short`   |       整数        |    2     |   (2)    |
| `i`  |        `int`         |       整数        |    4     |   (2)    |
| `I`  |    `unsigned int`    |       整数        |    4     |   (2)    |
| `l`  |        `long`        |       整数        |    4     |   (2)    |
| `L`  |   `unsigned long`    |       整数        |    4     |   (2)    |
| `q`  |     `long long`      |       整数        |    8     |   (2)    |
| `Q`  | `unsigned long long` |       整数        |    8     |   (2)    |
| `n`  |      `ssize_t`       |       整数        |          |   (3)    |
| `N`  |       `size_t`       |       整数        |          |   (3)    |
| `e`  |         (6)          |       float       |    2     |   (4)    |
| `f`  |       `float`        |       float       |    4     |   (4)    |
| `d`  |       `double`       |       float       |    8     |   (4)    |
| `s`  |       `char[]`       |      字节串       |          |          |
| `p`  |       `char[]`       |      字节串       |          |          |
| `P`  |       `void *`       |       整数        |          |   (5)    |

格式字符之前可以带有整数重复计数。 例如，格式字符串 `'4h'` 的含义与 `'hhhh'` 完全相同。

格式之间的空白字符会被忽略；但是计数及其格式字符中不可有空白字符。

对于 `'s'` 格式字符，计数会被解析为字节的长度，而不是像其他格式字符那样的重复计数；例如，`'10s'` 表示一个 10 字节的字节串，而 `'10c'` 表示 10 个字符。 如果未给出计数，则默认值为 1。 对于打包操作，字节串会被适当地截断或填充空字节以符合要求。 对于解包操作，结果字节对象总是恰好具有指定数量的字节。 作为特殊情况，`'0s'` 表示一个空字符串（而 `'0c'` 表示 0 个字符）。

```python
import struct

# 用于解析文件以及网络的二进制数据
if __name__ == '__main__':
    buffer = struct.pack('ii', 1, 2)  # 默认会使用字节对其
    print(buffer)
    for item in struct.iter_unpack('i', buffer):  # 每次解包struct.calcsize('i')个字节
        print(type(item), item)
```

# 函数

- *exception*  `struct.error`

  会在多种场合下被引发的异常；其参数为一个描述错误信息的字符串。

- `struct.pack`(*format*, *v1*, *v2*, *...*)

  返回一个 bytes 对象，其中包含根据格式字符串 *format* 打包的值 *v1*, *v2*, ... 参数个数必须与格式字符串所要求的值完全匹配。

- `struct.pack_into`(*format*, *buffer*, *offset*, *v1*, *v2*, *...*)

  根据格式字符串 *format* 打包 *v1*, *v2*, ... 等值并将打包的字节串写入可写缓冲区 *buffer* 从 *offset* 开始的位置。 请注意 *offset* 是必需的参数。

- `struct.unpack`(*format*, *buffer*)

  根据格式字符串 *format* 从缓冲区 *buffer* 解包（假定是由 `pack(format, ...)` 打包）。 结果为一个元组，即使其只包含一个条目。 缓冲区的字节大小必须匹配格式所要求的大小，如 [`calcsize()`](https://docs.python.org/zh-cn/3.8/library/struct.html#struct.calcsize) 所示。

- `struct.unpack_from`(*format*, *buffer*, *offset=0*)

  对 *buffer* 从位置 *offset* 开始根据格式字符串 *format* 进行解包。 结果为一个元组，即使其中只包含一个条目。 缓冲区的字节大小从位置 *offset* 开始必须至少为 [`calcsize()`](https://docs.python.org/zh-cn/3.8/library/struct.html#struct.calcsize) 显示的格式所要求的大小。

- `struct.iter_unpack`(*format*, *buffer*)

  根据格式字符串 *format* 以迭代方式从缓冲区 *buffer* 解包。 此函数返回一个迭代器，它将从缓冲区读取相同大小的块直至其内容全部耗尽。 缓冲区的字节大小必须整数倍于格式所要求的大小，如 [`calcsize()`](https://docs.python.org/zh-cn/3.8/library/struct.html#struct.calcsize) 所示。每次迭代将产生一个如格式字符串所指定的元组。

- `struct.calcsize`(*format*)

  返回与格式字符串 *format* 相对应的结构的大小（亦即 `pack(format, ...)` 所产生的字节串对象的大小）。

# 类

*class* `struct.Struct`(*format*)

返回一个新的 Struct 对象，它会根据格式字符串 *format* 来写入和读取二进制数据。**一次性地创建 Struct 对象并调用其方法相比使用同样的格式调用 [struct](https://docs.python.org/zh-cn/3.8/library/struct.html#module-struct) 函数更为高效** ，因为这样格式字符串只需被编译一次。