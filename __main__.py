print(__name__)
import argparse
parser = argparse.ArgumentParser(
    description = '''Три различных генератора имён.''')

#{{{
parser.add_argument('-p', '--path',
    help = '''Путь к файлу с базовым списком имён.
    Имена должны быть записаны по одному на строку''')
parser.add_argument('-s', '--source',
    nargs = '+',
    help = 'Принимает список имён из командной строки.') 
parser.add_argument('-c', '--count',
    type = int,
    default = 1,
    help = 'Количество генерируемых имён.')
parser.add_argument('-l', '--length', '--max-length',
    dest = 'max_len',
    type = int,
    default = 10,
    help = 'Максимальная длина имени.')
parser.add_argument('-e', '--ends',
    nargs = '+',
    help = 'Принимает список окончаний из командной строки.') 
#}}}

args = parser.parse_args()

if args.ends: args.ends = tuple(args.ends)
if not (args.source or args.path):
    parser.print_help()
    exit(1)

source = None
if args.source: source = list(map(lambda s: s.rstrip() + end, args.source))
if args.path:
    with open(args.path) as f:
        source = f.readlines()

print(parts.generate(source, args.max_len, args.count, args.ends))
