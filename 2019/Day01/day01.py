import pytest

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("12", 2),
    ("14", 2),
    ("1969", 654),
    ("100756", 33583),
    ("12\n14\n1969\n100756", 34241),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("14", 2),
    ("1969", 966),
    ("100756", 50346),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def module_mass(mod):
    return max(0, (int(mod)//3)-2)


def partOne(inp):
    return sum(module_mass(mod.strip()) for mod in inp.split('\n'))


def partTwo(inp):
    all_fuel = 0
    for mod in inp.split('\n'):
        this_fuel = module_mass(mod.strip())
        all_fuel += this_fuel
        while this_fuel:
            this_fuel = module_mass(this_fuel)
            all_fuel += this_fuel
    return all_fuel


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
