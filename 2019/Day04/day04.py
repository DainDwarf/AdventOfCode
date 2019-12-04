from collections import Counter
import pytest

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    (111111, True),
    (223450, False),
    (123789, False),
])
def testCriteria(inp, exp):
    res = check_pass(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    (112233, True),
    (123444, False),
    (111122, True),
])
def testCriteria2(inp, exp):
    res = check_pass2(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def check_pass(i, minNum=100000, maxNum=999999):
    if not minNum <= i <= maxNum:
        return False
    s = list(str(i))
    if s != sorted(s): # Not increasing
        return False
    if len(s) == len(set(s)): # No double
        return False
    return True


def check_pass2(i, minNum=100000, maxNum=999999):
    if not minNum <= i <= maxNum:
        return False
    s = list(str(i))
    if s != sorted(s): # Not increasing
        return False
    return 2 in Counter(s).values()


def partOne(minNum, maxNum):
    sum = 0
    for i in range(minNum, maxNum+1):
        if check_pass(i):
            sum += 1
    return sum


def partTwo(minNum, maxNum):
    sum = 0
    for i in range(minNum, maxNum+1):
        if check_pass2(i):
            sum += 1
    return sum

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("min", help='Your input minimum', type=int)
    args.add_argument("max", help='Your input maximum', type=int)
    options = args.parse_args()

    print("Answer for part one is : {res}".format(res=partOne(options.min, options.max)))
    print("Answer for part two is : {res}".format(res=partTwo(options.min, options.max)))
