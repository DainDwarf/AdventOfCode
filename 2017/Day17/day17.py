#!/usr/bin/python3
from __future__ import print_function

class CircularBuffer(object):
    def __init__(self, step):
        self.__buf = [0]
        self.__cur = 0
        self.step = step

    def __str__(self):
        return ' '.join(str(n) if i != self.__cur else '('+str(n)+')' for (i, n) in enumerate(self.__buf))

    def __repr__(self):
        return str(self)

    def __getitem__(self, it):
        return self.__buf[it%len(self.__buf)]

    def doStep(self):
        new_cur = (self.__cur + self.step) % len(self.__buf)
        self.__buf.insert(new_cur+1, len(self.__buf))
        self.__cur = new_cur+1

    def index(self, ob):
        return self.__buf.index(ob)

def curGen(step, max_n):
    """Get cursor position at each iteration."""
    cur = 0
    buf_len = 1
    for i in range(max_n):
        yield cur
        cur = (cur+step)%buf_len
        buf_len += 1
        cur += 1


def genPosOne(step, max_n):
    for i, cur in enumerate(curGen(step, max_n)):
        if cur == 1:
            yield i


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = 3

    circ = CircularBuffer(ex)
    for i in range(10):
        print(circ)
        circ.doStep()

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")

    circ = CircularBuffer(ex)
    prev_next_0 = None
    for i in range(1, 1001):
        circ.doStep()
        if circ[1] != prev_next_0:
            prev_next_0 = circ[1]
            print("{i}: New num inserted at position 1 : {n}".format(i=i, n=circ[1]))

    for n in genPosOne(ex, 1000):
        print("{n}: Emulated, will be inserted at position 1: {n}".format(n=n))



def partOne(inp):
    circ = CircularBuffer(inp)
    for i in range(2017):
        circ.doStep()
    return circ[circ.index(2017)+1]


def partTwo(inp):
    """We do not use the circular buffer here, as it is too slow."""
    for n in genPosOne(inp, 50000000):
        pass
    return n

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input', type=int)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
