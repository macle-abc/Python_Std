# import argparse
# parser = argparse.ArgumentParser()

# 长选项, 默认会产生同名的位置参数eg: --verbosity string 这里的string即为verbosity的值
# parser.add_argument("--verbosity", help="increase output verbosity", action="store_true")
# args = parser.parse_args()
# if args.verbosity:
#     print("verbosity turned on")
#     print(args.verbosity)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")