import pytest


@pytest.mark.parametrize("inp, exp", [
    ("""101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603""", [
    [101, 102, 103],
    [301, 302, 303],
    [501, 502, 503],
    [201, 202, 203],
    [401, 402, 403],
    [601, 602, 603],
    ]),
])
def testTwo(inp, exp):
    res = list(by_column(inp))
    print(f"Test {inp} gives {res}")
    assert res == exp


def check_triangle(a, b, c):
    return ((a+b > c)
       and  (a+c > b)
       and  (b+c > a)
    )


def by_column(inp):
    acc1 = []
    acc2 = []
    acc3 = []
    for line in inp.strip().split('\n'):
        a, b, c = [int(i) for i in line.split()]
        acc1.append(a)
        acc2.append(b)
        acc3.append(c)
        if len(acc1) == 3:
            yield acc1
            yield acc2
            yield acc3
            acc1 = []
            acc2 = []
            acc3 = []



def partOne(inp):
    return sum(1 if check_triangle(*[int(i) for i in line.split()]) else 0
                for line in inp.strip().split('\n'))


def partTwo(inp):
    return sum(1 if check_triangle(*line) else 0
                for line in by_column(inp))


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
