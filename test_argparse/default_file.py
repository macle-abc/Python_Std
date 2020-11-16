import sys
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-infile', nargs='?', type=argparse.FileType('r'), const=sys.stdin,
                    default='fff.txt', help="默认fff.txt,如果指定了-infile但是没有传入infile将使用sys.stdin")
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
# print(parser.parse_args(['input.txt', 'output.txt']))

print(parser.print_help())
# args = parser.parse_args(['ff.txt'])
# print(args)
# args.outfile.write(args.infile.read())
