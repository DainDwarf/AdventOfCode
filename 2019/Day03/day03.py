import pytest

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("R8,U5,L5,D3\nU7,R6,D4,L4", 6),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 159),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("R8,U5,L5,D3\nU7,R6,D4,L4", 30),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 610),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def gen_positions(path):
    x = y = 0
    yield(0, 0)
    for instruction in path.split(','):
        direction = instruction[0]
        length = int(instruction[1:])
        for i in range(length):
            if direction == 'R':
                x += 1
            elif direction == 'L':
                x -= 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            yield (x, y)


def manhattan(pos):
    return sum(abs(i) for i in pos)


def partOne(inp):
    path1, path2 = inp.split('\n')
    pos1 = set(gen_positions(path1))
    pos2 = set(gen_positions(path2))
    return min(manhattan(pos) for pos in pos1.intersection(pos2) if pos != (0, 0))


def partTwo(inp):
    path1, path2 = inp.split('\n')
    pos1 = list(gen_positions(path1))
    pos2 = list(gen_positions(path2))
    intersections = set(pos1).intersection(set(pos2)) - {(0, 0)}
    return min(pos1.index(p)+pos2.index(p) for p in intersections)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
