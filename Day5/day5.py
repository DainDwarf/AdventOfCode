#!/usr/bin/python
from __future__ import print_function

def _runCode(instructions):
    pointer = 0
    pointers_list = []
    try:
        while True:
            jump = instructions[pointer]
            instructions[pointer] +=1
            pointers_list.append(pointer)
            pointer += jump
    except IndexError:
        pass
    return pointers_list


def runCode(text):
    return _runCode(list(map(int, text.strip().split('\n'))))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    instructions="""0
3
0
1
-3
"""
    print("Unit testing part One.")
    run = runCode(instructions)
    print("It took {num} steps to get out of code, following steps {run}".format(
        num=len(run)
        , run=run
    ))

def partOne(inp):
    return len(runCode(inp))

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
