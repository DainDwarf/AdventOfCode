import pytest

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def partOne(inp):
    pass


def partTwo(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
