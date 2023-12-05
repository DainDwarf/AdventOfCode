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
    (97, False),
    (98, True),
    (99, True),
    (100, False),
])
def test_interval(inp, exp):
    inter = Interval(98, 2)
    assert (inp in inter) == exp


@pytest.mark.parametrize("inp, exp", [
    (97, 97),
    (98, 50),
    (99, 51),
    (100, 100),
])
def test_intermap(inp, exp):
    imap = InterMap.from_input("50 98 2")
    assert imap[inp] == exp


@pytest.mark.parametrize("inp, exp", [
    ((97, 1), [(97, 1)]),
    ((98, 1), [(50, 1)]),
    ((99, 1), [(51, 1)]),
    ((100, 1), [(100, 1)]),
    ((97, 4), [(97, 1), (50, 2), (100, 1)]),
])
def test_intermap_interval(inp, exp):
    imap = InterMap.from_input("50 98 2")
    assert imap.multiple(Interval(*inp)) == [Interval(*t) for t in exp]


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


@pytest.mark.skip
def test_two():
    res = part_two(TEST_EXAMPLE)
    assert res == 46


class Interval:
    __start = 0
    __end = 0

    @property
    def start(self): return self.__start

    @property
    def end(self): return self.__end

    def __init__(self, start: int, length: int = 1):
        self.__start = start
        self.__end = start + length - 1

    def __hash__(self):
        return hash((self.__start, self.__end))

    def __repr__(self):
        return f"({self.__start}, {self.__end})"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __len__(self):
        return self.__end - self.__start + 1

    def __contains__(self, x: int):
        return self.__start <= x <= self.__end
    
    def __getitem__(self, index: int):
        if self.__start + index <= self.__end:
            return self.__start + index
        else:
            raise IndexError("Interval index out of range")

    def index(self, x: int):
        if x in self:
            return x - self.__start
        else:
            return ValueError(f"{x} is not in Interval {self}")


class InterMap:
    __source = None
    __dest = None

    def __init__(self, source: Interval, dest: Interval):
        self.__source = source
        self.__dest = dest

    @classmethod
    def from_input(cls, inp: str):
        dest, source, length = map(int, inp.split())
        return cls(Interval(source, length), Interval(dest, length))

    def __contains__(self, x: int):
        return x in self.__source

    def __getitem__(self, x: int):
        if x in self.__source:
            return self.__dest[self.__source.index(x)]
        else:
            return x

    def multiple(self, inter: Interval):
        """Translate an input interval into a list of intervals according to the translation table."""
        if inter.end < self.__source.start:
            return [inter]
        elif inter.start > self.__source.end:
            return [inter]
        else: # There is an intersection somewhere
            ret = []
            if inter.start < self.__source.start: # Some untouched left part
                ret.append(Interval(inter.start, self.__source.start-inter.start))
            # Middle part
            mid_start = max(inter.start, self.__source.start)
            mid_end = min(inter.end, self.__source.end)
            length = mid_end-mid_start+1
            ret.append(Interval(self[mid_start], length))
            if inter.end > self.__source.end: # Some untouched right part
                ret.append(Interval(self.__source.end+1, inter.end-self.__source.end))
            return ret


class Mapping:
    __intermaps = None

    def __init__(self):
        self.__intermaps = []

    @classmethod
    def from_input(cls, inp: str):
        self = cls()
        for line in inp.split('\n'):
            self.__intermaps.append(InterMap.from_input(line))
        return self

    def __getitem__(self, x: int):
        for i in self.__intermaps:
            if x in i:
                return i[x]
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
