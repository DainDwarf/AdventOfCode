import pytest
from intcode.simulator import Simulator, ParamMode


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


def part_one(code):
    tractor = dict()
    for x in range(50):
        for y in range(50):
            sim = Simulator(code)
            sim.add_input([x, y])
            sim.run()
            tractor[x, y] = sim.output()[0]
    for y in range(50):
        for x in range(50):
            print('.' if tractor[x, y] == 0 else '#', end='')
        print()
    return sum(tractor.values())


def part_two(code):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(code)))
    print("Answer for part two is : {res}".format(res=part_two(code)))
