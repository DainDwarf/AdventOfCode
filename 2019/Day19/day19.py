import pytest
import math
from intcode.simulator import Simulator, ParamMode


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


def get_preview(code, start=(0, 0), size=50):
    start_x, start_y = start
    tractor = dict()
    for x in range(start_x, start_x+size):
        for y in range(start_y, start_y+size):
            sim = Simulator(code)
            sim.add_input([x, y])
            sim.run()
            tractor[x, y] = sim.output()[0]
    return tractor


def part_one(preview):
    return sum(preview.values())


def display(preview):
    minx = min(p[0] for p in preview.keys())
    maxx = max(p[0] for p in preview.keys())
    miny = min(p[1] for p in preview.keys())
    maxy = max(p[1] for p in preview.keys())
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            cell = preview.get((x, y), 0)
            print('.' if cell == 0 else '#', end='')
        print()


def horizontal(preview, y):
    """Get the x start and end of the horizontal at row ``y``."""
    maxx = max(p[0] for p in preview.keys())
    horizontal_x = [x for x in range(maxx+1) if preview[x, y] == 1]
    return min(horizontal_x), max(horizontal_x)


def get_largest_horizontal(preview):
    """Get the largest horizontal fully visible in preview."""
    maxy = max(p[1] for p in preview.keys())
    maxx = max(p[0] for p in preview.keys())
    for y in range(maxy+1):
        if preview[maxx, y] == 1:
            return (y-1,) + horizontal(preview, y-1)
    return (maxy,) + horizontal(preview, maxy)


def vertical(preview, x):
    """Get the y start and end of the vertical at column ``x``."""
    maxy = max(p[1] for p in preview.keys())
    vertical_y = [y for y in range(maxy+1) if preview[x, y] == 1]
    return min(vertical_y), max(vertical_y)


def get_largest_vertical(preview):
    """Get the largest vertical fully visible in preview."""
    maxy = max(p[1] for p in preview.keys())
    maxx = max(p[0] for p in preview.keys())
    for x in range(maxx+1):
        if preview[x, maxy] == 1:
            return (x-1,) + vertical(preview, x-1)
    return (maxx,) + vertical(preview, maxx)


def approximate_position_of_row(preview, size):
    """Based on the start of the tractor beam, approximate the row where you have a horizontal of a given size."""
    y, x_start, x_end = get_largest_horizontal(preview)
    x_size = x_end-x_start+1
    # Intercept theorem to the rescue!
    # x_size / size == (0-(x_start,y)) / (0-(far_x, far_y))
    # (0-(x_start,y)) / (0-(far_x, far_y)) == (0-(0, y)) / (0-(0, far_y))
    # far_y = size/x_size * y
    far_y = size/x_size * y
    # (0, (0, y)) / (0-(0, far_y))  == x_start / far_x
    far_x = x_start*far_y/y
    return int(far_x), int(far_y)


def approximate_position_of_column(preview, size):
    """Based on the start of the tractor beam, approximate the column where you have a vertical of a given size."""
    x, y_start, y_end = get_largest_vertical(preview)
    y_size = y_end-y_start+1
    far_x = size/y_size*x
    far_y = y_start*far_x/x
    return int(far_x), int(far_y)


def part_two(preview, code):
    x1, y1 = approximate_position_of_column(preview, 200)
    x2, y2 = approximate_position_of_row(preview, 200)
    print(x1, y1)
    print(x2, y2)
    # far_preview = get_preview(code, (x, y), 200)
    # display(far_preview)
    far_preview = get_preview(code, (825, 1025), 200)
    display(far_preview)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    preview = get_preview(code)
    display(preview)
    print("Answer for part one is : {res}".format(res=part_one(preview)))
    print("Answer for part two is : {res}".format(res=part_two(preview, code)))
