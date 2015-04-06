__all__ = ['parts', 'kana', 'norse']

from . import parts, kana, norse

from os import path
from random import choice, random
from string import whitespace

get_max = lambda words: max(len(word) for word in words)

def get_data_dir():
    if path.isdir('data'):
        return 'data'
    elif platform.startswith('linux'):
        d = getenv('XDG_DATA_HOME')
        if d: return path.join(d, 'jang')
        else: return path.join(getenv('HOME'),'.local/share/jang')

def get_words(filename, data):
    words = None
    filepath = path.join(data, filename)
    with open(filepath, encoding='utf-8') as f:
        words = f.readlines()
    return words

def single_name(nat, gender, chance = 0.1, datapath = get_data_dir()):
    names = get_words('{}_{}.txt'.format(nat, gender), datapath)
    thnames = get_words('{}_thname.txt'.format(nat), datapath)

    if random() > chance:
        name = choice(names).strip(',' + whitespace).capitalize()
        thname = choice(thnames).strip(',' + whitespace).capitalize()
    else:
        max_len = get_max(names)
        name = parts.generate(names, max_len, 1)[0]

        max_len = get_max(thnames)
        thname = parts.generate(thnames, max_len, 1)[0]

    return '{} {}'.format(name, thname)
