#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    (97, 97),
    (98, 50),
    (99, 51),
    (100, 100),
])
def test_interval(inp, exp):
    inter = Interval.from_input("50 98 2")
    assert inter.offset(inp)+inp == exp


@pytest.mark.parametrize("inp, exp", [
    (79, 81),
    (14, 14),
    (55, 57),
    (13, 13),
])
def test_mapping(inp, exp):
    mapp = Mapping.from_input("50 98 2\n52 50 48")
    assert mapp[inp] == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


class Interval:
    __start = 0
    __end = 0
    __offset = 0

    def __init__(self, source: int, dest: int, length: int):
        self.__start = source
        self.__end = source + length - 1
        self.__offset = dest - source

    @classmethod
    def from_input(cls, inp: str):
        dest, source, length = map(int, inp.split())
        return cls(source, dest, length)

    def __contains__(self, x):
        return self.__start <= x <= self.__end

    def offset(self, x):
        if x in self:
            return self.__offset
        else:
            return 0


class Mapping:
    __intervals = None

    def __init__(self):
        self.__intervals = []

    @classmethod
    def from_input(cls, inp: str):
        self = cls()
        for line in inp.split('\n'):
            self.__intervals.append(Interval.from_input(line))
        return self

    def __getitem__(self, x: int):
        for i in self.__intervals:
            if x in i:
                return x+i.offset(x)
        return x


def part_one(inp):
    pass


def part_two(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
