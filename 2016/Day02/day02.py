import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("""
ULL
RRDDD
LURDL
UUUUD""", '1985'),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("""
ULL
RRDDD
LURDL
UUUUD""", '5DB3'),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def crack(inp, grid, pos):
    for line in inp.strip().split('\n'):
        for direction in line:
            if direction == 'U':
                next_pos = (pos[0]-1, pos[1])
            elif direction == 'D':
                next_pos = (pos[0]+1, pos[1])
            elif direction == 'R':
                next_pos = (pos[0], pos[1]+1)
            elif direction == 'L':
                next_pos = (pos[0], pos[1]-1)
            else:
                raise RuntimeError(f"Unknown direction {direction}")
            if next_pos in grid:
                pos = next_pos
        yield grid[pos]


def partOne(inp):
    grid = {(0, 0): '1',
            (0, 1): '2',
            (0, 2): '3',
            (1, 0): '4',
            (1, 1): '5',
            (1, 2): '6',
            (2, 0): '7',
            (2, 1): '8',
            (2, 2): '9',
    }
    pos = (1, 1)
    return ''.join(crack(inp, grid, pos))


def partTwo(inp):
    grid = {(0, 2): '1',
            (1, 1): '2',
            (1, 2): '3',
            (1, 3): '4',
            (2, 0): '5',
            (2, 1): '6',
            (2, 2): '7',
            (2, 3): '8',
            (2, 4): '9',
            (3, 1): 'A',
            (3, 2): 'B',
            (3, 3): 'C',
            (4, 2): 'D',
    }
    pos = (2, 0)
    return ''.join(crack(inp, grid, pos))


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
