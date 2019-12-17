import pytest
from itertools import islice, repeat

import numpy as np


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    (38, 8),
    (-17, 7),
])
def test_normalization(inp, exp):
    res = normalize(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp_list", [
    (0, [1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1]),
    (1, [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]),
    (2, [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1]),
])
def test_pattern_generation(inp, exp_list):
    res_gen = generate_pattern(inp)
    for exp, res in zip(exp_list, res_gen):
        assert res == exp


def test_fft_matrix():
    inp = "12345678"
    exp = np.array([
        [ 1,  0, -1,  0,  1,  0, -1,  0],
        [ 0,  1,  1,  0,  0, -1, -1,  0],
        [ 0,  0,  1,  1,  1,  0,  0,  0],
        [ 0,  0,  0,  1,  1,  1,  1,  0],
        [ 0,  0,  0,  0,  1,  1,  1,  1],
        [ 0,  0,  0,  0,  0,  1,  1,  1],
        [ 0,  0,  0,  0,  0,  0,  1,  1],
        [ 0,  0,  0,  0,  0,  0,  0,  1],
    ])
    res = get_fft_matrix(inp)
    assert np.array_equal(res, exp)


@pytest.mark.parametrize("inp, steps, exp", [
    ("12345678", 1, "48226158"),
    ("12345678", 2, "34040438"),
    ("12345678", 3, "03415518"),
    ("12345678", 4, "01029498"),
    ("80871224585914546619083218645595", 100, "24176176"),
    ("19617804207202209144916044189917", 100, "73745418"),
    ("69317163492948606335995924319873", 100, "52432133"),
])
def test_part_one(inp, steps, exp):
    res = part_one(inp, steps)
    assert res == exp


def normalize(n):
    return abs(n) % 10


def generate_pattern(i):
    yield from repeat(0, i)
    while True:
        yield from repeat(1, i+1)
        yield from repeat(0, i+1)
        yield from repeat(-1, i+1)
        yield from repeat(0, i+1)


def get_fft_matrix(inp):
    rows = []
    dimension = len(inp.strip())
    for i in range(dimension):
        this_row = list(islice(generate_pattern(i), dimension))
        rows.append(this_row)
    return np.array(rows)


def part_one(inp, steps=100):
    fft = get_fft_matrix(inp)
    inp = np.array(list(map(int, inp)))
    for _ in range(steps):
        inp = np.vectorize(normalize)(fft @ inp)
    return ''.join(map(str, inp))[:8]


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
