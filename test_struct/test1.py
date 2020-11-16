import struct

# 用于解析文件以及网络的二进制数据
if __name__ == '__main__':
    buffer = struct.pack('ii', 1, 2)  # 默认会使用字节对其
    print(buffer)
    for item in struct.iter_unpack('i', buffer):  # 每次解包struct.calcsize('i')个字节
        print(type(item), item)
