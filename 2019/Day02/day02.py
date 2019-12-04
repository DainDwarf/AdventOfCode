import pytest

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
    ("1,0,0,0,99", "2,0,0,0,99"),
    ("2,3,0,3,99", "2,3,0,6,99"),
    ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
    ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
])
def testSimulation(inp, exp):
    simulator = Simulator(inp)
    simulator.run()
    res = simulator.state()
    print(f"Test {inp} gives {res}")
    assert res == exp


class Simulator:
    def __init__(self, inp):
        self._state = [int(i) for i in inp.split(',')]
        self._cp = 0
        self._finished = False

    def __getitem__(self, pos):
        return self._state[pos]

    def __setitem__(self, pos, value):
        self._state[pos] = value

    def _step(self):
        """Runs a single step."""
        if self._finished:
            return

        op_code = self[self._cp]
        if op_code == 1:
            self[self[self._cp+3]] = self[self[self._cp+2]] + self[self[self._cp+1]]
        elif op_code == 2:
            self[self[self._cp+3]] = self[self[self._cp+2]] * self[self[self._cp+1]]
        elif op_code == 99:
            self._finished = True
        else:
            raise ValueError(f"Unkown OP code: {op_code}")
        self._cp += 4

    def run(self):
        while not self._finished:
            self._step()

    def state(self):
        return ",".join(str(i) for i in self._state)

def partOne(inp):
    simulator = Simulator(inp)
    simulator[1] = 12
    simulator[2] = 2
    simulator.run()
    return simulator[0]


def partTwo(inp, target):
    """Let's brute force"""
    for noun in range(100):
        for verb in range(100):
            simulator = Simulator(inp)
            simulator[1] = noun
            simulator[2] = verb
            simulator.run()
            if simulator[0] == target:
                return 100*noun+verb


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--target", help='Target number for part 2', type=int)
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp, options.target)))
