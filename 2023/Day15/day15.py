#!/usr/bin/python3
from collections import defaultdict, OrderedDict
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("HASH", 52),
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
])
def test_xmash(inp, exp):
    assert xmash(inp) == exp

def test_one():
    assert part_one("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 1320

def test_two():
    assert part_two("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 145

def xmash(string):
    ret = 0
    for c in string:
        ret += ord(c)
        ret *= 17
        ret %= 256
    return ret


def part_one(inp):
    return sum(xmash(step) for step in inp.split(','))


def part_two(inp):
    hashmap = OrderedDict()

    # No need to actually put everything in boxes yet
    for step in inp.split(','):
        if '=' in step:
            label, focal = step.split('=')
            hashmap[label] = int(focal)
        elif '-' in step:
            label = step[:-1]
            hashmap.pop(label, None)

    #NOW put them in boxes
    boxes = defaultdict(list)
    for label, focal in hashmap.items():
        boxes[xmash(label)].append(focal)

    #Compute
    ret = 0
    for boxnum, lenses in sorted(boxes.items(), key=lambda t: t[0]):
        for slot, focal in enumerate(lenses, 1):
            ret += (1+boxnum)*slot*focal 
    return ret


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
