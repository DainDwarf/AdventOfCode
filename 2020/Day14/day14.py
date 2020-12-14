#!/usr/bin/python3
import re
from itertools import zip_longest


def apply_mask(mask, num):
    for i, m in enumerate(mask[::-1]):
        if m == '1':
            num |= 1 << i
        elif m == '0':
            num &= ~(1 << i)
    return num


def apply_mask_v2(mask, num):
    ret = []
    for m, n in zip_longest(mask[::-1], bin(num)[:1:-1]):
        if m == '0':
            ret.append(n if n is not None else '0')
        else:
            ret.append(m if m is not None else '0')
    return ''.join(reversed(ret))


def x_gen(addr_spec):
    def _sub_gen(current_num=0, current_index=0):
        for i, m in enumerate(addr_spec[-1-current_index::-1], current_index):
            if m == '1':
                current_num += 1<<i
            elif m == 'X':
                yield from _sub_gen(current_num, i+1)
                yield from _sub_gen(current_num + (1 << i), i+1)
                return
        yield current_num
    return _sub_gen()


class Bitmask:
    def __init__(self):
        self._mem = dict()
        self._mask = "X"

    def set_mask(self, mask):
        self._mask = mask

    def write_mem(self, mem, num):
        self._mem[mem] = apply_mask(self._mask, num)

    def parse_line(self, line):
        if line.startswith("mask"):
            self.set_mask(line.split(' = ')[1])
        else:
            mem, num = re.match(r"mem\[(\d+)\] = (\d+)", line).groups()
            self.write_mem(int(mem), int(num))

    def sum(self, inp):
        for line in inp.split('\n'):
            self.parse_line(line)
        return sum(self._mem.values())


class BitmaskV2(Bitmask):
    def write_mem(self, mem, num):
        for m in x_gen(apply_mask_v2(self._mask, mem)):
            self._mem[m] = num


def part_one(inp):
    return Bitmask().sum(inp)


def part_two(inp):
    return BitmaskV2().sum(inp)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
