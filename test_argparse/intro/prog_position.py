# import argparse
# parse = argparse.ArgumentParser()
# parse.add_argument("echo", help="echo the string you use here")
# args = parse.parse_args()
# print(args.echo)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number", type=float)
args = parser.parse_args()
print(args.square**2)
