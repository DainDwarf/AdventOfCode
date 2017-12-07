#!/usr/bin/python
from __future__ import print_function

def redistribute(old_banks):
    banks = old_banks[:]
    biggest_i = banks.index(max(banks))
    to_give = banks[biggest_i]
    banks[biggest_i]=0
    for i in range(biggest_i+1, to_give+biggest_i+1):
        banks[i%len(banks)] += 1
    return banks

def runUntilCycle(banks):
    previous_banks = []
    while banks not in previous_banks:
        previous_banks.append(banks)
        banks = redistribute(banks)
    return previous_banks

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    banks=[0, 2, 7, 0]

    run = runUntilCycle(banks)
    print("Running debugger One, it took {num} steps to get a cycle, following steps {run}".format(
        num=len(run)
        , run=run
    ))

def partOne(inp):
    return len(runUntilCycle(list(map(int, inp.strip().split()))))

def partTwo(inp):
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
