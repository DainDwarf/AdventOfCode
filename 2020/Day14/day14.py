#!/usr/bin/python3
import re


def apply_mask(mask, num):
    for i, m in enumerate(mask[::-1]):
        if m == '1':
            num |= 1 << i
        elif m == '0':
            num &= ~(1 << i)
    return num


class Bitmask:
    def __init__(self):
        self._mem = dict()
        self._mask = "X"

    def set_mask(self, mask):
        self._mask = mask

    def parse_line(self, line):
        if line.startswith("mask"):
            self.set_mask(line.split(' = ')[1])
        else:
            mem, num = re.match(r"mem\[(\d+)\] = (\d+)", line).groups()
            self._mem[int(mem)] = apply_mask(self._mask, int(num))

    def part_one(self, inp):
        for line in inp.split('\n'):
            self.parse_line(line)
        return sum(self._mem.values())


def part_one(inp):
    return Bitmask().part_one(inp)


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
