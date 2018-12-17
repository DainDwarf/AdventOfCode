import re


def addr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]+reg[regB]
    return reg

def addi(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]+regB
    return reg

def mulr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]*reg[regB]
    return reg

def muli(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]*regB
    return reg

def banr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]&reg[regB]
    return reg

def bani(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]&regB
    return reg

def borr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]|reg[regB]
    return reg

def bori(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]|regB
    return reg

def setr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = reg[regA]
    return reg

def seti(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = regA
    return reg

def gtir(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if regA > reg[regB] else 0
    return reg

def gtri(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if reg[regA] > regB else 0
    return reg

def gtrr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if reg[regA] > reg[regB] else 0
    return reg

def eqir(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if regA == reg[regB] else 0
    return reg

def eqri(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if reg[regA] == regB else 0
    return reg

def eqrr(reg, regA, regB, regC):
    reg = reg[:]
    reg[regC] = 1 if reg[regA] == reg[regB] else 0
    return reg


class OpInfer(object):
    def __init__(self):
        self.opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
        assert len(self.opcodes) == 16
        self.translation = dict() #opcode : op

    def getMatchingOP(self, inp, display=False):
        nums = list(map(int, re.findall(r'(-?\d+)', inp)))
        before = nums[0:4]
        rule   = nums[4:8]
        after  = nums[8:12]
        matches = []
        for op in self.opcodes:
            if op(before, *rule[1:]) == after:
                matches.append(op)
                if display:
                    print("Opcode {code} could be {op}.".format(code=rule[0], op=op.__name__))
        return rule[0], matches

    def countMatchingOP(self, inp, display=False):
        return len(self.getMatchingOP(inp, display)[1])

    def matchOneOPCode(self, inp):
        """Get a certainly matching op code."""
        inp = inp.split('\n\n')
        for r in inp:
            opcode, op = self.getMatchingOP(r)
            if len(op) == 1:
                return opcode, op[0]

    def getOPCodes(self, inp):
        match = self.matchOneOPCode(inp)
        while match is not None:
            opcode, op = match
            print(f"Assuming op {op.__name__} is opcode {opcode}.")
            assert opcode not in self.translation
            self.translation[opcode] = op
            self.opcodes.remove(op)
            match = self.matchOneOPCode(inp)
        return self.translation


class Computer(object):
    def __init__(self, opcodes):
        self.codes = opcodes
        assert all(i in self.codes for i in range(16))
        self.reg = [0, 0, 0, 0]

    def step(self, instruction):
        nums = list(map(int, instruction.strip().split()))
        self.reg = self.codes[nums[0]](self.reg, *nums[1:])

    def execute(self, code):
        for i in code.split('\n'):
            self.step(i)


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""
    num = OpInfer().countMatchingOP(inp, display=True)

    print(f"There are {num} opcodes that could match the example.")

    res = partOne(inp)
    print(f"This means there are {res} input with 3 or more matching opcodes in the example.")


def testTwo():
    print("No unit test for Part Two!")


def partOne(inp):
    inp = inp.split('\n\n')
    return sum(1 if OpInfer().countMatchingOP(r) >= 3 else 0 for r in inp)


def partTwo(samples, code):
    op_translation = OpInfer().getOPCodes(inp)
    comp = Computer(op_translation)
    comp.execute(code)
    return comp.reg[0]


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-1", dest="samples", help='Your samples file', type=FileType('r'))
    args.add_argument("-2", dest="code", help='Your code file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.samples:
        inp = options.samples.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        if options.code:
            code = options.code.read().strip()
            print("Answer for part two is : {res}".format(res=partTwo(inp, code)))
