#!/usr/bin/python3
from __future__ import print_function

searching = { 'children'    : lambda v: v==3
            , 'cats'        : lambda v: v==7
            , 'samoyeds'    : lambda v: v==2
            , 'pomeranians' : lambda v: v==3
            , 'akitas'      : lambda v: v==0
            , 'vizslas'     : lambda v: v==0
            , 'goldfish'    : lambda v: v==5
            , 'trees'       : lambda v: v==3
            , 'cars'        : lambda v: v==2
            , 'perfumes'    : lambda v: v==1
}

retroencabulator =  { 'children'    : lambda v: v==3
                    , 'cats'        : lambda v: v>7
                    , 'samoyeds'    : lambda v: v==2
                    , 'pomeranians' : lambda v: v<3
                    , 'akitas'      : lambda v: v==0
                    , 'vizslas'     : lambda v: v==0
                    , 'goldfish'    : lambda v: v<5
                    , 'trees'       : lambda v: v>3
                    , 'cars'        : lambda v: v==2
                    , 'perfumes'    : lambda v: v==1
}

class Sue(object):
    def __init__(self, description):
        head, params = description.split(': ', 1)
        self.num = int(head.split()[1])
        self.params = dict() 
        for p in params.split(', '):
            name, num = p.split(': ')
            self.params[name] = int(num)

    def isCorresponding(self, filt=searching):
        return all(filt[k](v) for k, v in self.params.items())

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = "toto"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))

def genSues(inp, filt):
    for line in inp.split('\n'):
        sue = Sue(line)
        if sue.isCorresponding(filt):
            yield sue.num

def partOne(inp):
    return list(genSues(inp, searching))

def partTwo(inp):
    return list(genSues(inp, retroencabulator))

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
