#!/usr/bin/python3
from __future__ import print_function
from collections import Counter
import itertools

# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

def testTwo():
    ex = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""

    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    twos = 0
    threes = 0
    for word in inp.split('\n'):
        c = Counter(word.strip())
        twos += 1 if 2 in c.values() else 0
        threes += 1 if 3 in c.values() else 0
    return twos * threes

def difference(w1, w2):
    """Returns the number of differing caracters between two same-length strings."""
    return sum(c1!=c2 for c1, c2 in zip(w1, w2))

def getOneCharDiffs(inp):
    words = [w.strip() for w in inp.split('\n')]
    for w1, w2 in itertools.combinations(words, 2):
        if difference(w1, w2) == 1:
            yield w1, w2

def partTwo(inp):
    diffs = [t for t in getOneCharDiffs(inp)]
    assert len(diffs) == 1
    w1, w2 = diffs[0]
    similar = ""
    for c1, c2 in zip(w1, w2):
        if c1 == c2:
            similar += c1
    return similar


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
