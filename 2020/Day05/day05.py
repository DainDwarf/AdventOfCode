#!/usr/bin/python3
import pytest


def seat_id(board):
    to_binary = str.maketrans('BFRL', '1010')
    return int(board.translate(to_binary), base=2)


def part_one(inp):
    return max(seat_id(line) for line in inp.split('\n'))


def part_two(inp):
    seats_taken = sorted([seat_id(line) for line in inp.split('\n')])
    for i, seat in enumerate(seats_taken, start=min(seats_taken)):
        if i != seat:
            return i


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
