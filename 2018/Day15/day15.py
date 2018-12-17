
target_example = """######
#E..G.#
#...#.#
#.G.#G#
#######"""


move_example = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""

combat_example = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""

combat_example2 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""

combat_example3 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""

combat_example4 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""

combat_example5 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""

combat_example6 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = "toto"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")


def testTwo():
    print("Unit test for Part Two.")

    inp = "toto"
    res = partTwo(inp)
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
