__all__ = ['parts', 'kana', 'norse']

from . import parts, kana, norse

from os import path, getenv
from random import choice, random
from string import whitespace

# TODO
def get_max(words):
    return max(len(word) for word in words)

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
        max_len = get_max(names)
        name = parts.generate(names, max_len, 1)

        max_len = get_max(thnames)
        thname = parts.generate(thnames, max_len, 1)

    return '{} {}'.format(name, thname)
