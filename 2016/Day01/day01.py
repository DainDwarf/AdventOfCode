import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("R2, L3", 5),
    ("R2, R2, R2", 2),
    ("R5, L5, R5, R3", 12),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("R8, R4, R4, R8", 4),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def partOne(inp):
    position = (0, 0)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction = 0
    for instruction in inp.strip().split(', '):
        turn = instruction[0]
        walk = int(instruction[1:])
        direction = (direction + (1 if turn == 'R' else -1)) % 4
        position = (position[0]+directions[direction][0]*walk,
                    position[1]+directions[direction][1]*walk,
        )
    return abs(position[0])+abs(position[1])


def partTwo(inp):
    previous_pos = set()
    position = (0, 0)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction = 0
    for instruction in inp.strip().split(', '):
        turn = instruction[0]
        walk = int(instruction[1:])
        direction = (direction + (1 if turn == 'R' else -1)) % 4
        for _ in range(walk):
            previous_pos.add(position)
            position = (position[0]+directions[direction][0],
                        position[1]+directions[direction][1],
            )
            if position in previous_pos:
                return abs(position[0])+abs(position[1])


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
