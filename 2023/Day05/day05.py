#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


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
    (79, 82),
    (14, 43),
    (55, 86),
    (13, 35),
])
def test_pathing(inp, exp):
    mappings_inp = TEST_EXAMPLE.split('\n', 2)[-1]
    pathing = all_mappings(mappings_inp)
    x = inp
    fro = ''
    to = 'seed'
    while to in pathing:
        fro = to
        to, mapp = pathing[to]
        x = mapp[x]
    assert x == exp


def test_one():
    res = part_one(TEST_EXAMPLE)
    assert res == 35


def test_two():
    res = part_two(TEST_EXAMPLE)
    assert res == 46


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


def all_mappings(mappings_inp):
    """Returns a dict that maps an input category to a tuple (destination category, Mapping)"""
    ret = {}
    for block in mappings_inp.split('\n\n'):
        name, desc = block.split('\n', 1)
        fro, _, to = name.split()[0].split('-')
        ret[fro] = (to, Mapping.from_input(desc))
    return ret


def part_one(inp):
    seeds_inp, mappings_inp = inp.split('\n\n', 1)
    pathing = all_mappings(mappings_inp)
    seeds = [int(x) for x in seeds_inp.split(':')[1].split()]
    locations = []
    for x in seeds:
        fro = ''
        to = 'seed'
        while to in pathing:
            fro = to
            to, mapp = pathing[to]
            x = mapp[x]
        locations.append(x)
    return min(locations)


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
