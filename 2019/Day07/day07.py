import pytest
from itertools import cycle, permutations
from intcode.simulator import Operation, Simulator


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("code, phases, exp", [
    ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", (4,3,2,1,0), 43210),
    ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", (0,1,2,3,4), 54321),
    ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", (1,0,4,3,2), 65210),
])
def test_amplifiers(code, phases, exp):
    res = simul_amplifiers(code, phases)
    print(f"Test {code} gives {res}")
    assert res == exp


@pytest.mark.parametrize("code, exp", [
    ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210),
    ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", 54321),
    ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", 65210),
])
def testOne(code, exp):
    res = partOne(code)
    print(f"Test {code} gives {res}")
    assert res == exp


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("code, phases, exp", [
    ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", (9,8,7,6,5), 139629729),
    ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", (9,7,8,5,6), 18216),
])
def test_feedback(code, phases, exp):
    res = simul_feedback(code, phases)
    print(f"Test {code} gives {res}")
    assert res == exp


@pytest.mark.parametrize("code, exp", [
    ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", 139629729),
    ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", 18216),
])
def testTwo(code, exp):
    res = partTwo(code)
    print(f"Test {code} gives {res}")
    assert res == exp


def simul_amplifiers(code, phases):
    signal = 0
    for p in phases:
        sim = Simulator(code, inp=[p, signal])
        sim.run()
        signal = sim.output()[0]
    return signal


def partOne(code):
    return max(simul_amplifiers(code, phases) for phases in permutations(range(5)))


def simul_feedback(code, phases):
    signal = 0
    amplifiers = [Simulator(code, inp=[p]) for p in phases]
    for i, sim in enumerate(cycle(amplifiers)):
        sim.add_input([signal])
        sim.run(until=Operation.OUTPUT)
        signal = sim.output()[-1]
        if all(s.finished for s in amplifiers):
            return signal


def partTwo(code):
    return max(simul_feedback(code, phases) for phases in permutations(range(5, 10)))


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(code)))
    print("Answer for part two is : {res}".format(res=partTwo(code)))
