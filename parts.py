#!/usr/bin/python
from random import choice
from random import randrange

def name_parts(name):
    """Разбивает данную строку на подстроки из трёх символов.

    'Василий' --> ['аси', 'сил', 'или', 'лий', 'ий ']
    """
    return [name[i:i+3] for i in range(1,len(name)-2)]

def name_from_parts(source, name_part, max_count, end = ' '):
    """Генерирует имя из предоставленных частей, с заданной максимальной длинной."""

    name = choice(source)[:3]
    for i in range(1, max_count - 1):
        contlist = set(filter(lambda x: x.startswith(name[i:i+2]), name_part))
        if len(contlist) != 0:
            name += choice(tuple(contlist))[2]
        if name.endswith(end):
            break
    return name

def concat_end(name, end):
    """Добавляет окончание к слову.

    Добавляет одно из двух окончаний к слову.
    Если слово заканчивается частью одного из окончаний, то дополняет до
    полного окончания.
    """

    if not end: return name

    if name.endswith(end):
        if randrange(1): # 50%-я замена одного окончания на другое
            if name.endswith(end[0]):
                name = name[:name.rfind(end[0])] + end[1]
            else:
                name = name[:name.rfind(end[1])] + end[0]
    else:
        for k in range(len(end[0]), 0, -1):
            if name.endswith(end[0][:k]):
                name += end[0][k:]
                break
        else:
            for k in range(len(end[1]), 0, -1):
                if name.endswith(end[1][:k]):
                    name += end[1][k:]
                    break
            else:
                name += choice(end)
    return name

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description = '''Три различных генератора имён.''')


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

    args = parser.parse_args()

    if args.ends: args.ends = tuple(args.ends)
    if not (args.source or args.path):
        parser.print_help()
        exit(1)

    source = None
    end = ' '
    if args.source: source = list(map(lambda s: s.rstrip() + end, args.source))
    if args.path: with open(args.path) as f: source = f.readlines()
    count = args.count
    max_len = args.max_len
    ends = args.ends 

    name_part = set(part for name in source for part in name_parts(name))
    names = [name_from_parts(source, name_part, max_len, end = end)
            for i in range(count)]
    for name in names:
        name = concat_end(name, ends)

    print('\n'.join(names).title())

if __name__ == '__main__': main()
