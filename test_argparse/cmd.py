import argparse
import os

if __name__ == '__main__':
    parse = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parse.add_argument('cmd', help="需要执行的命令")
    parse.add_argument('args', nargs=argparse.REMAINDER, help="用于传递给cmd的参数")
    args = parse.parse_args()
    cmd = []
    for item in args.args:
        cmd.append(item)
    cmd = " ".join(cmd)
    cmd = f"{args.cmd} {cmd}"
    os.system(cmd)
