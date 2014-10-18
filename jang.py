#!/usr/bin/python
from random import choice
from random import randrange
END = ' '

def name_parts(name):
    """Разбивает данную строку на подстроки из трёх символов.

    'Василий' --> ['аси', 'сил', 'или', 'лий', 'ий ']
    """
    return [name[i:i+3] for i in range(1,len(name)-2)]

def concat_end(name, end):
    """Добавляет окончание к слову.

    Добавляет одно из двух окончаний к слову.
    Если слово заканчивается частью одного из окончаний, то дополняет до
    полного окончания.
    """

    if end == None: return name

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

def name_from_parts(source, name_part, max_count):
    """Генерирует имя из предоставленных частей, с заданной максимальной длинной."""

    name = choice(source)[:3]
    for i in range(1, max_count - 1):
        contlist = set(filter(lambda x: x.startswith(name[i:i+2]), name_part))
        if len(contlist) != 0:
            name += choice(tuple(contlist))[2]
        if name.endswith(END):
            break
    return name

def prepare_source(source):
    if isinstance(source, str):
        with open(source) as f: source = f.readlines()
    if isinstance(source, list):
        return list(map(lambda s: s.rstrip() + END, source))
    else:
        return None

#{{{ Non-standart generator
def japan_name(max_len):
    """Генерирует японское имя, собирая его из каны."""

    parts = (  'а',  'и',  'у',  'э',  'о',  'я',  'ю',  'ё',
              'ка', 'ки', 'ку', 'кэ', 'ко', 'кя', 'кю', 'кё',
              'са', 'си', 'су', 'сэ', 'со', 'ся', 'сю', 'сё',
              'та', 'ти', 'цу', 'тэ', 'то', 'тя', 'тю', 'тё',
              'на', 'ни', 'ну', 'нэ', 'но', 'ня', 'ню', 'нё',
              'ха', 'хи', 'фу', 'хэ', 'хо', 'хя', 'хю', 'хё',
              'ма', 'ми', 'му', 'мэ', 'мо', 'мя', 'мю', 'мё',
              'ра', 'ри', 'ру', 'рэ', 'ро', 'ря', 'рю', 'рё',
              'ва',                                          'н',
              'га', 'ги', 'гу', 'гэ', 'го', 'гя', 'гю', 'гё',
             'дза','дзи','дзу','дзэ','дзо','дзя','дзю','дзё',
              'да',             'дэ', 'до',
              'ба', 'би', 'бу', 'бэ', 'бо', 'бя', 'бю', 'бё',
              'па', 'пи', 'пу', 'пэ', 'по', 'пя', 'пю', 'пё')
    name = ''
    for i in range(randrange(2,max_len/2)):
        name += choice(parts)
    return name

def norvey_male_name(ends):
    """Генерирует норвежское имя из типичных начал и окончаний."""

    start = ("ас","ауд","атли","арн","аль","аг",
             "барди","берси","бёд","болли","бруни",
             "ве","вагни","вик","ван","валь","варди",
             "гуди","вест","гунн","гейр","бранд","бьёрн",
             "гест","гисл","грин","гуд","инг","кнуд","колль",
             "магни","мар","мод","отт","одд","орм","раг","рауд",
             "рун","свейн","сиг","свер","скег","снор","стейн",
             "снэ","тор","трюг","ульв","фрид","фрей","хальф",
             "хар","хрут","хаук","хьяр","эй","хольм","хельм")
    end = ("бьёрн","ун","мунд","ульв","вальд","льот",
           "рик","гейр","вёр","бранд","грим","мод","ланд",
           "гард","ар","мар","рёд","лейв","бейн","стейн",
           "фред","аринн","гест","гисл","одд","винд")

    name = choice(start)
    if not name.endswith(('и','ь','е','э','й')):
        if (not randrange(5) and not ends):  #TODO: более ясно описать 80%-е добавление "и"
            if name[-1] == name[-2]:
                name += 'и'
            else:
                name += name[-1] + 'и'
        else:
            name += choice(end)
    else:
        name += choice(end)
    return concat_end(name,ends)
#}}}

#{{{ For argparse arguments
def universal(source, count, max_len, ends = None):
    source = prepare_source(source)
    name_part = set(part for name in source for part in name_parts(name))
    names = [name_from_parts(source, name_part, max_len) for i in range(count)]
    for name in names:
        name = concat_end(name, ends)
    return names

def japan(source, count, max_len, ends = None):
    names = [japan_name(max_len) for i in range(count)]
    for name in names:
        name = concat_end(name, ends)
    return names

def viking(source, count, max_len, ends = None):
    return [norvey_male_name(ends) for i in range(count)]
#}}}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = '''Три различных генератора имён.''')
    #{{{ Generator selection
    parser.add_argument('-1', '--first', '-u', '--universal',
        action = 'store_const',
        const = universal,
        dest = 'generator',
        help = '''Универсальный генератор.
            Генерирует новое имя или список имён на основе предоставленного
            списка. При необходимости можно указать шанс выбора для вывода
            имён из исходного списка.
        '''
        )
    parser.add_argument('-2', '--second', '-j', '--japan',
        action = 'store_const',
        const = japan,
        dest = 'generator',
        help = '''Для имён, подобных японским.
            Собирает имя из каны. Вполне вероятно, что значения полученное имя
            иметь не будет. Между тем, для европейца получаемые имена звучат
            вполне "по-восточному".
        '''
        )
    parser.add_argument('-3', '--third', '-v', '--viking',
        action = 'store_const',
        const = viking,
        dest = 'generator',
        help = '''Для скандинавских имён.
            Выбирает случайное начало и добавляет случайное окончание из двух
            заранее определённых списков. Полученное имя не только звучит, но и
            может быть переведено (т.е. имеет некое значение).
        '''
        )
    #}}}

    #{{{ Source names
    parser.add_argument('--preset',
        default = None,
        help = 'Имя заранее готового набора опций.')
    parser.add_argument('-p', '--path',
        dest = 'source',
        help = '''Путь к файлу с базовым списком имён.
        Имена должны быть записаны по одному на строку''')
    parser.add_argument('-s', '--source',
        dest = 'source',
        nargs = '+',
        help = 'Принимает список имён из командной строки.') 
    parser.add_argument('-c', '--count',
        dest = 'count',
        type = int,
        default = 1,
        help = 'Количество генерируемых имён.')
    parser.add_argument('-l', '--length', '--max-length',
        dest = 'max_len',
        type = int,
        default = 10,
        help = 'Максимальная длина имени.')
    parser.add_argument('-e', '--ends',
        dest = 'ends',
        nargs = '+',
        help = 'Принимает список окончаний из командной строки.') 
    #}}}

    args = parser.parse_args()

    if args.preset:
        config = json.load('config.json')

    if args.ends: args.ends = tuple(args.ends)

    if (not args.source
        and args.generator != japan
        and args.generator != viking):
        parser.print_help()
        exit(1)

    if args.generator == None:
        result = universal(args.source, args.count, args.max_len, ends = args.ends)
    else:
        result = args.generator(args.source, args.count, args.max_len, ends = args.ends)
        
    print('\n'.join(result).title())
