#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
class TestDay01:
    inp = """1721
979
366
299
675
1456"""
    def test_one(self):
        res = part_one(self.inp)
        assert res == 514579


    def test_two(self):
        res = part_two(self.inp)
        assert res == 241861950


def parse(inp):
    return [int(line) for line in inp.strip().split('\n')]


def part_one(inp):
    lili = parse(inp)
    for num in lili:
        if 2020-num in lili:
            return num*(2020-num)


def part_two(inp):
    lili = parse(inp)
    for num1 in lili:
        for num2 in lili:   # TODO: Avoid nums before num1
            if 2020-num1-num2 in lili:
                return num1*num2*(2020-num1-num2)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
