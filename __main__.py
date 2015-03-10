from random import choice, random
from string import whitespace
from os import path, getenv

# TODO
def get_max(nat, name):
    if nat == 'eng' and not name:
        return 10
    elif nat == 'eng' and name:
        return 6
    else:
        return 10

# TODO for windows
def get_data_dir():
    d = getenv('XDG_DATA_HOME')
    if d: return path.join(d, 'jang')
    else: return path.join(getenv('HOME'),'.local/share/jang')

def get_words(filename):
    words = None
    filepath = path.join(get_data_dir(), filename)
    with open(filepath) as f:
        words = f.readlines()
    return words

def single_name(nat, gender, chance = 0.1):
    names = get_words('{}_{}.txt'.format(nat, gender))
    thnames = get_words('{}_thname.txt'.format(nat))

    if random() > chance:
        name = choice(names).strip(',' + whitespace).capitalize()
        thname = choice(thnames).strip(',' + whitespace).capitalize()
    else:
        max_len = get_max(nat, True)
        name = parts.gen_names(names, max_len, 1)

        max_len = get_max(nat, False)
        thname = parts.gen_names(thnames, max_len, 1)

    return '{} {}'.format(name, thname)

#TODO
def main ():
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

    print(generate(source, args.max_len, args.count, args.ends))

if __name__ = "__main__":
    print(dir())
    #main()
