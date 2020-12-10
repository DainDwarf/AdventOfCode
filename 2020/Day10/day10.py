#!/usr/bin/python3
from itertools import groupby


def tribonacci(n):
    """
    Computes the ``n``th term of the suite defined by:
        u_{n+1} = u_n + u_{n-1} + u_{n-2}

    with u_1 = 1, u_2 = 2, u_3 = 4.

    It's like Fibonacci, but with an extra lookup.
    It's called the Tribonacci sequence.
    """
    a, b, c = 1, 2, 4
    if n==1: return a
    if n==2: return b
    if n==3: return c
    for i in range(n-3):
        a, b, c = b, c, a+b+c
    return c


def get_adjacency_list(inp):
    so = sorted(map(int, inp.split('\n')))
    return [y-x for x, y in zip([0] + so, so + [so[-1]+3])]


def part_one(inp):
    adj = get_adjacency_list(inp)
    return adj.count(1) * adj.count(3)


def part_two(inp):
    adj = get_adjacency_list(inp)
    # It seems AoC is nice with us and only gives us adjacencies of 1 or 3.
    # But I put a warning here in case you have a non-nice input.
    assert adj.count(1)+adj.count(3) == len(adj)
    paths = 1
    for num, group in groupby(adj):
        if num == 1:
            paths *= tribonacci(len(list(group)))
    return paths


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
