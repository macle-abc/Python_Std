import argparse

# 创建解释器, epilog 在-h后显示的额外信息，allow_abbrev默认允许长选项的缩写，eg:--sum可以写成-s
parser = argparse.ArgumentParser(description='Process some integers.', epilog="??", allow_abbrev=False)
# metavar命令行提示显示的变量名
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
# dest存储到accumulate
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
