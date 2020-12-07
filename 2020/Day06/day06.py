#!/usr/bin/python3
from collections import Counter


def part_one(inp):
    count = 0
    for group in inp.split('\n\n'):
        count += len(set(group.replace('\n', '')))
    return count


def part_two(inp):
    count = 0
    for group in inp.split('\n\n'):
        group_len = len(group.split('\n'))
        for letter, occurrence in Counter(group).items():
            if occurrence == group_len:
                count += 1
    return count


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
