# That's handy, the Advent of Code gives unittests.
def testOne():
    inp = "toto"
    res = partOne(inp)

    print("Unit test for Part One.")
    print(f"Test {inp} gives {res}")


def testTwo():
    inp = "toto"
    res = partTwo(inp)

    print("Unit test for Part Two.")
    print(f"Test {inp} gives {res}")


def partOne(inp):
    pass


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
