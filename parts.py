from random import choice

def to_parts(name):
    """Разбивает данную строку на подстроки из трёх символов.

    'Василий' --> ['аси', 'сил', 'или', 'лий', 'ий ']
    """
    return [name[i:i+3] for i in range(1,len(name)-2)]

def name_from_parts(source, name_parts, max_count, end = ' '):
    """Генерирует имя из предоставленных частей, с заданной максимальной длинной."""

    name = choice(source)[:3]
    for i in range(1, max_count - 1):
        contlist = set(filter(lambda x: x.startswith(name[i:i+2]), name_parts))
        if len(contlist) != 0:
            name += choice(tuple(contlist))[2]
        if name.endswith(end):
            break
    return name.strip(end)

def concat_end(name, end):
    """Добавляет окончание к слову.

    Добавляет одно из двух окончаний к слову.
    Если слово заканчивается частью одного из окончаний, то дополняет до
    полного окончания.
    """

    if not end: return name

    if name.endswith(end):
        if choice([True, False]): # 50%-я замена одного окончания на другое
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

def generate(src, max_length, count, ends = None, end = ','):
    parts = set(part for name in src for part in to_parts(name))
    names = [name_from_parts(src, parts, max_length, end = end)
            for i in range(count)]
    for name in names:
        name = concat_end(name, ends)

    return names
