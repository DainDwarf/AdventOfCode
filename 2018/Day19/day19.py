class WatchCPU(object):
    """CPU modelization of that weird watch."""
    def __init__(self):
        self.reg = [0]*6
        self.ip = 0
        self.bound = None
        self.code = []

    def bindIP(self, regN):
        """Bind the instruction pointer to the given register number."""
        self.bound = regN

    def parseCode(self, code):
        """Parse the code, without the instruction bounding operation."""
        self.code = []
        code = code.strip().split('\n')
        if code[0].startswith('#'):
            bind = int(code[0].split()[1])
            self.bindIP(bind)
            code = code[1:]
        for line in code:
            instruction, *operands = line.split()
            self.code.append([instruction] + list(map(int, operands)))

    def step(self, debug=False):
        """Simulates a CPU cycle.

        Use debug=True to display the state of ip, registers and instruction."""
        if self.ip < 0 or self.ip >= len(self.code):
            #Avoid looping through python negative indexes.
            raise IndexError
        if self.bound is not None:
            self.reg[self.bound] = self.ip
        if debug:
            print(f"ip={self.ip} {self.reg} ", end='')

        instruction, *operands = self.code[self.ip]
        getattr(self, instruction)(*operands)

        if debug:
            print(f"{instruction} {operands} {self.reg}")
        if self.bound is not None:
            self.ip = self.reg[self.bound]

        self.ip += 1

    #All instructions, quite boring really.
    def addr(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]+self.reg[regB]

    def addi(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]+regB

    def mulr(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]*self.reg[regB]

    def muli(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]*regB

    def banr(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]&self.reg[regB]

    def bani(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]&regB

    def borr(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]|self.reg[regB]

    def bori(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]|regB

    def setr(self, regA, regB, regC):
        self.reg[regC] = self.reg[regA]

    def seti(self, regA, regB, regC):
        self.reg[regC] = regA

    def gtir(self, regA, regB, regC):
        self.reg[regC] = 1 if regA > self.reg[regB] else 0

    def gtri(self, regA, regB, regC):
        self.reg[regC] = 1 if self.reg[regA] > regB else 0

    def gtrr(self, regA, regB, regC):
        self.reg[regC] = 1 if self.reg[regA] > self.reg[regB] else 0

    def eqir(self, regA, regB, regC):
        self.reg[regC] = 1 if regA == self.reg[regB] else 0

    def eqri(self, regA, regB, regC):
        self.reg[regC] = 1 if self.reg[regA] == regB else 0

    def eqrr(self, regA, regB, regC):
        self.reg[regC] = 1 if self.reg[regA] == self.reg[regB] else 0


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

    watch = WatchCPU()
    watch.parseCode(inp)
    for _ in range(5):
        watch.step(debug=True)

    res = partOne(inp)
    print(f"Register 0 contains {res} at the end.")


def testTwo():
    print("No unit test for Part Two!")


def partOne(inp, debug=False):
    watch = WatchCPU()
    watch.parseCode(inp)
    try:
        while True:
            watch.step(debug=debug)
    except IndexError:
        return watch.reg[0]


def partTwo(inp, debug=False):
    watch = WatchCPU()
    watch.parseCode(inp)
    watch.reg[0] = 1
    try:
        while True:
            watch.step(debug=debug)
    except IndexError:
        return watch.reg[0]


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    args.add_argument("-d", "--debug", help='Print debugging information', action="store_true")
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp, debug=options.debug)))
        print("I will not be able to compute the solution for part 2, that is not the goal of today. But you can see the debug trace...")
        partTwo(inp, debug=options.debug)
