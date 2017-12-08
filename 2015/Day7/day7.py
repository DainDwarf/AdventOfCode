#!/usr/bin/python3
from __future__ import print_function
import re

class Emulator(object):
    """Ok, follow me here...

    To create lazy-gates on the fly, we will create classes that can access emulator's wires by closure...
    in the following, 'self' refers to the pointer to current Emulator object,
    while 'this' refers to the pointer to created gate that uses closure to access 'self' (i.e. the emulator)
    """

    def __init__(self):
        self.wires = dict()
        self.values_cache = dict() #Instead of recomputing every wire's value, keep it in another dictionary.

    def getValue(self, wire_name):
        if wire_name in self.values_cache.keys():
            return self.values_cache[wire_name]
        else:
            ret = None
            try:
                ret = self.wires[wire_name].getValue()
            except KeyError: #OK, this one is a dirty hack, because problem was ill-specified!
                ret = int(wire_name)
            self.values_cache[wire_name] = ret
            return ret

    def addValue(self, wire_name, value):
        class Value(object):
            def __init__(this, value):
                this.value = value

            def getValue(this):
                return this.value
        self.wires[wire_name] = Value(value)

    def addNot(self, wire_name, input_name):
        class Not(object):
            def __init__(this, input_name):
                this.inp = input_name

            def getValue(this):
                """16-bits bit-wise negation."""
                return (2**16-1)^(self.getValue(this.inp))
        self.wires[wire_name] = Not(input_name)

    def addAssign(self, wire_name, input_name):
        """I'm not sure this instruction exists, but anyway..."""
        class Assign(object):
            def __init__(this, input_name):
                this.inp = input_name

            def getValue(this):
                return self.getValue(this.inp)
        self.wires[wire_name] = Assign(input_name)

    def addLShift(self, wire_name, input_name, amount):
        class LShift(object):
            def __init__(this, input_name, amount):
                this.inp = input_name
                this.n = amount

            def getValue(this):
                return (self.getValue(this.inp) << this.n) % (2**16)
        self.wires[wire_name] = LShift(input_name, amount)

    def addRShift(self, wire_name, input_name, amount):
        class RShift(object):
            def __init__(this, input_name, amount):
                this.inp = input_name
                this.n = amount

            def getValue(this):
                return self.getValue(this.inp) >> this.n
        self.wires[wire_name] = RShift(input_name, amount)

    def addAnd(self, wire_name, l_name, r_name):
        class And(object):
            def __init__(this, l_name, r_name):
                this.l = l_name
                this.r = r_name

            def getValue(this):
                return self.getValue(this.l) & self.getValue(this.r)
        self.wires[wire_name] = And(l_name, r_name)

    def addOr(self, wire_name, l_name, r_name):
        class Or(object):
            def __init__(this, l_name, r_name):
                this.l = l_name
                this.r = r_name

            def getValue(this):
                return self.getValue(this.l) | self.getValue(this.r)
        self.wires[wire_name] = Or(l_name, r_name)

def emulate(instructions):
    emu = Emulator()

    value_re = r"(\d+) -> (\w+)"
    assign_re = r"(\w+) -> (\w+)"
    not_re = r"NOT (\w+) -> (\w+)"
    lshift_re = r"(\w+) LSHIFT (\d+) -> (\w+)"
    rshift_re = r"(\w+) RSHIFT (\d+) -> (\w+)"
    and_re = r"(\w+) AND (\w+) -> (\w+)"
    or_re = r"(\w+) OR (\w+) -> (\w+)"

    for line in instructions:
        if re.match(value_re, line):
            value, wire_name = re.match(value_re, line).groups()
            emu.addValue(wire_name, int(value))
        elif re.match(assign_re, line):
            in_name, wire_name = re.match(assign_re, line).groups()
            emu.addAssign(wire_name, in_name)
        elif re.match(not_re, line):
            in_name, wire_name = re.match(not_re, line).groups()
            emu.addNot(wire_name, in_name)
        elif re.match(lshift_re, line):
            in_name, amount, wire_name = re.match(lshift_re, line).groups()
            emu.addLShift(wire_name, in_name, int(amount))
        elif re.match(rshift_re, line):
            in_name, amount, wire_name = re.match(rshift_re, line).groups()
            emu.addRShift(wire_name, in_name, int(amount))
        elif re.match(and_re, line):
            l_name, r_name, wire_name = re.match(and_re, line).groups()
            emu.addAnd(wire_name, l_name, r_name)
        elif re.match(or_re, line):
            l_name, r_name, wire_name = re.match(or_re, line).groups()
            emu.addOr(wire_name, l_name, r_name)
        else:
            raise RuntimeError("Unrecognized instruction {l}".format(l=line))
    return emu


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    from random import shuffle
    ex = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

    print("Unit test for Part One.")
    instructions = ex.split('\n')
    shuffle(instructions)

    emu = emulate(instructions)
    print("{r}: {val}".format(r='d', val=emu.getValue('d')))
    print("{r}: {val}".format(r='e', val=emu.getValue('e')))
    print("{r}: {val}".format(r='f', val=emu.getValue('f')))
    print("{r}: {val}".format(r='g', val=emu.getValue('g')))
    print("{r}: {val}".format(r='h', val=emu.getValue('h')))
    print("{r}: {val}".format(r='i', val=emu.getValue('i')))
    print("{r}: {val}".format(r='x', val=emu.getValue('x')))
    print("{r}: {val}".format(r='y', val=emu.getValue('y')))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    return emulate(inp.split('\n')).getValue('a')

def partTwo(inp):
    pass

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
