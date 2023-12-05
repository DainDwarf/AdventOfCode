#!/usr/bin/python3
from itertools import batched
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
    inter = Interval(98, 99)
    assert (inp in inter) == exp


def test_interlist():
    li = InterList()
    li.add(Interval(0, 100))
    assert li == [Interval(0, 100)]
    li.add(Interval(103, 200))
    assert li == [Interval(0, 100), Interval(103, 200)]
    li.add(Interval(97, 150))
    assert li == [Interval(0, 200)]
    li.cut(Interval(90, 110))
    assert li == [Interval(0, 89), Interval(111, 200)]
    li.cut(Interval(100, 123))
    assert li == [Interval(0, 89), Interval(124, 200)]


@pytest.mark.parametrize("inp, exp", [
    (97, 97),
    (98, 50),
    (99, 51),
    (100, 100),
])
def test_intermap(inp, exp):
    imap = InterMap.from_input("50 98 2")
    assert imap[inp] == exp


@pytest.mark.skip
@pytest.mark.parametrize("inp, exp", [
    ((97, 97), [(97, 97)]),
    ((98, 98), [(50, 50)]),
    ((99, 99), [(51, 51)]),
    ((100, 100), [(100, 100)]),
    ((97, 100), [(97, 97), (50, 51), (100, 100)]),
])
def test_intermap_interval(inp, exp):
    imap = InterMap.from_input("50 98 2")
    assert imap.multiple(Interval(*inp)) == [Interval(*t) for t in exp]


@pytest.mark.skip
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

    def __init__(self, start: int, end: int):
        self.__start = start
        self.__end = end

    def __hash__(self):
        return hash((self.__start, self.__end))

    def __repr__(self):
        return f"({self.__start}, {self.__end})"

    def __str__(self):
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

    def intersect(self, other):
        return self.start <= other.end and self.end >= other.start

    @classmethod
    def union(cls, inter1, inter2):
        assert inter1.intersect(inter2)
        return cls(min(inter1.start, inter2.start), max(inter1.end, inter2.end))


class InterList:
    __intervals = None

    def __init__(self):
        self.__intervals = set()

    def add(self, new: Interval):
        overlap = None
        for i in self.__intervals:
            if i.intersect(new):
                overlap = i
                break
        if overlap is not None:
            self.__intervals.remove(overlap)
            return self.add(Interval.union(new, overlap))
        else:
            self.__intervals.add(new)

    def cut(self, old: Interval):
        overlaps = []
        for i in self.__intervals:
            if i.intersect(old):
                overlaps.append(i)
        for over in overlaps:
            self.__intervals.remove(over)
            if over.start < old.start:
                self.__intervals.add(Interval(over.start, old.start-1))
            if over.end > old.end:
                self.__intervals.add(Interval(old.end+1, over.end))

    def __iter__(self):
        return iter(self.__intervals)

    def __eq__(self, other):
        return all(i in other for i in self.__intervals)


class InterMap:
    __source = None
    __dest = None

    def __init__(self, source: Interval, dest: Interval):
        self.__source = source
        self.__dest = dest

    @classmethod
    def from_input(cls, inp: str):
        dest, source, length = map(int, inp.split())
        return cls(Interval(source, source+length-1), Interval(dest, dest+length-1))

    def __contains__(self, x: int):
        return x in self.__source

    def __getitem__(self, x: int):
        if x in self.__source:
            return self.__dest[self.__source.index(x)]
        else:
            return x


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
    seeds_inp, mappings_inp = inp.split('\n\n', 1)
    seeds_inp = seeds_inp.split(':')[1].split()

    pathing = all_mappings(mappings_inp)
    seeds_intervals = [Interval(s, s+r-1) for s, r in batched(map(int, seeds_inp), n=2)]

    fro = ''
    to = 'seed'

    print(to)
    for s in sorted(seeds_intervals, key= lambda s:s.start):
        print(s)
    print('\n\n')

    while to in pathing:
        fro = to
        to, mapp = pathing[to]
        new_intervals = []
        for inter in seeds_intervals:
            new_intervals += mapp.multiple(inter)
        seeds_intervals = new_intervals

        print(to)
        for s in sorted(seeds_intervals, key= lambda s:s.start):
            print(s)
        print('\n\n')

    return min(i.start for i in seeds_intervals)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
