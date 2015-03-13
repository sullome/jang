__all__ = ['parts', 'kana', 'norse']

from . import parts, kana, norse

from os import path, getenv, listdir
from random import choice, random
from string import whitespace

get_max = lambda words: max(len(word) for word in words)

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

def check_full(files, nat):
    if files.count(nat) < 3:
        return False
    else:
        return True

def get_allnat(datapath = get_data_dir()):
    files = listdir(datapath)
    nats = set()
    checklist = []
    for f in files:
        f = f.split('_')[0]
        nats.add(f)
        checklist.append(f)
    nats = list(nat for nat in nats if check_full(checklist, nat))
    return nats

def single_name(nat, gender, chance = 0.1):
    names = get_words('{}_{}.txt'.format(nat, gender))
    thnames = get_words('{}_thname.txt'.format(nat))

    if random() > chance:
        name = choice(names).strip(',' + whitespace).capitalize()
        thname = choice(thnames).strip(',' + whitespace).capitalize()
    else:
        max_len = get_max(names)
        name = parts.generate(names, max_len, 1)[0]

        max_len = get_max(thnames)
        thname = parts.generate(thnames, max_len, 1)[0]

    return '{} {}'.format(name, thname)
