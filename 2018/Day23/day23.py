import re


def manhattan(p1, p2):
    return sum(map(lambda t: abs(t[0]-t[1]), zip(p1, p2)))


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

    res = partOne(inp)
    print(f"Example answer is {res}.")


def testTwo():
    print("Unit test for Part Two.")

    inp = "toto"
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")


def partOne(inp):
    num_re = r"(-?\d+)"
    bots = []
    for line in inp.split('\n'):
        x, y, z, r = list(map(int, re.findall(num_re, line)))
        bots.append(((x, y, z), r))
    best_bot, bot_range = max(bots, key=lambda t:t[1])
    return sum(1 if manhattan(b, best_bot) <= bot_range else 0 for b, _ in bots)


def partTwo(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
