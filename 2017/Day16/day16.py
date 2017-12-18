#!/usr/bin/python3
from __future__ import print_function


def getProgs(end_char):
    return list(map(chr, range(ord('a'), ord(end_char)+1)))

def spin(progs, num):
    return progs[len(progs)-(num%len(progs)):] + progs[:len(progs)-(num%len(progs))]

def exchange(progs, pos1, pos2):
    progs[pos1], progs[pos2] = progs[pos2], progs[pos1]
    return progs

def partner(progs, name1, name2):
    pos1 = progs.index(name1)
    pos2 = progs.index(name2)
    return exchange(progs, pos1, pos2)

def orderParse(progs, order):
    if order.startswith('s'):
        return spin(progs, int(order[1:]))
    elif order.startswith('x'):
        pos1, pos2 = map(int, order[1:].split('/'))
        return exchange(progs, pos1, pos2)
    elif order.startswith('p'):
        name1, name2 = order[1:].split('/')
        return partner(progs, name1, name2)
    else:
        raise RuntimeError("Unknown order {order}".format(order=order))

def dance(progs, inp):
    for order in inp.strip().split(','):
        progs = orderParse(progs, order)
    return progs

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex_progs = getProgs('e')
    ex = "s1,x3/4,pe/b"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex, 'e')))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex, 'e')))


def partOne(inp, end_char='p'):
    progs = getProgs(end_char)
    return ''.join(dance(progs, inp))

def partTwo(inp, end_char='p'):
    progs = getProgs(end_char)
    start_progs = getProgs(end_char)
    total_dances = 1000000000

    for i in range(total_dances):
        if progs == start_progs and i != 0:
            break #Found a cycle! Use it to fast forward.
        progs = dance(progs, inp)

    if i != total_dances-1:
        for i in range(total_dances%i):
            progs = dance(progs, inp)

    return ''.join(progs)

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
