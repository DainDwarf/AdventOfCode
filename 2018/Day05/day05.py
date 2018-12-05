#!/usr/bin/python3
from __future__ import print_function
import re


ALPHABET = ''.join(chr(c) for c in range(ord('A'), ord('Z')+1))
alphabet = ALPHABET.lower()
reaction_re = re.compile(
    '(' + '|'.join(c+C for c, C in zip(alphabet, ALPHABET)) +
    '|' + '|'.join(C+c for c, C in zip(alphabet, ALPHABET)) +
    ')')


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = 'dabAcCaCBAcCcaDA'

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))


def testTwo():
    ex = 'dabAcCaCBAcCcaDA'
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def react(inp):
    hasChanged = True
    while hasChanged:
        inp, hasChanged = reaction_re.subn('', inp)
    return inp

def partOne(inp):
    return len(react(inp))


def partTwo(inp):
    # High level optimization: You get the same result if you iterate over
    # the 26 possibilities on the already reduced input instead of the much
    # bigger real input
    inp = react(inp)

    improvements = dict()
    for c in alphabet:
        sub_inp, _ = re.subn("({c}|{C})".format(c=c, C=c.upper()), '', inp)
        improvements[c] = partOne(sub_inp)

    return min(improvements.values())


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
