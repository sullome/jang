__all__ = ['parts', 'kana', 'norse']

from . import parts, kana, norse

from os import path, getenv
from random import choice, random
from string import whitespace

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

def get_allnat(datapath = get_data_dir()):
    pass

def single_name(nat, gender, chance = 0.1):
    names = get_words('{}_{}.txt'.format(nat, gender))
    thnames = get_words('{}_thname.txt'.format(nat))

    if random() > chance:
        name = choice(names).strip(',' + whitespace).capitalize()
        thname = choice(thnames).strip(',' + whitespace).capitalize()
    else:
        max_len = get_max(nat, True)
        name = parts.generate(names, max_len, 1)

        max_len = get_max(nat, False)
        thname = parts.generate(thnames, max_len, 1)

    return '{} {}'.format(name, thname)
