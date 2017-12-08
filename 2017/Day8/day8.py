#!/usr/bin/python3
from __future__ import print_function
import re

#Syntax looks close to something you might do in python, so let's use exec!

def initVariables(instructions):
    """Get all variables in program, and return a dictionary of varname: 0."""
    get_var_names = r"^(\w+) \w+ [0-9+-]+ if (\w+)"
    all_used_vars = dict()
    for step in instructions:
        var1, var2 = re.match(get_var_names, step).groups()
        all_used_vars[var1] = 0
        all_used_vars[var2] = 0
    return all_used_vars

def formatInstructions(instructions):
    """Yield each instruction, so that they are suitable for exec.

    Variables are assumed to be hold in a dictionary named 'registers'.
    It will transform, for example,
        'a dec -10 if b != 5'
    by the instruction
        'registers['a'] -= -10 if registers['b'] != 5 else 0'
    """
    format_re = r"^(\w+) (\w+ [0-9+-]+ if) (\w+) (.*)"
    formatted_re = r"registers['\1'] \2 registers['\3'] \4"
    for step in instructions:
        registered_step = re.sub(format_re, formatted_re, step)
        registered_step = registered_step.replace(' inc ', ' += ') #Use spaces around inc, to avoid translate a register 'inc'.
        registered_step = registered_step.replace(' dec ', ' -= ')
        yield registered_step + " else 0"


def runInstructions(instructions):
    """Returns a dict of register:values after running the list of string instructions."""
    registers = initVariables(instructions)
    for line in formatInstructions(instructions):
        exec(line)
    return registers

def genHighestValues(instructions):
    """Yield highest value of registers at each step."""
    registers = initVariables(instructions)
    for line in formatInstructions(instructions):
        exec(line)
        yield max(registers.values())

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    example="""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

    print("Unit testing part one.")
    print("Highest register value is {res}".format(res=partOne(example)))
    print("All register values are {didi}".format(didi=runInstructions(example.strip().split('\n'))))

    print("")
    print("Unit testing part two.")
    print("Highest values at each step are {vals}".format(vals=list(genHighestValues(example.strip().split('\n')))))
    print("Highest ever value is {res}".format(res=partTwo(example)))

def partOne(inp):
    instructions = inp.strip().split('\n')
    registers = runInstructions(instructions)
    return max(registers.values())

def partTwo(inp):
    instructions = inp.strip().split('\n')
    return max(genHighestValues(instructions))

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
