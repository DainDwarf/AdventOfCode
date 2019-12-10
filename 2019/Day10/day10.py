import pytest
from math import gcd, atan2


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("x, y, exp", [
    (1, 0, 7),
    (4, 0, 7),
    (0, 2, 6),
    (1, 2, 7),
    (2, 2, 7),
    (3, 2, 7),
    (4, 2, 5),
    (4, 3, 7),
    (3, 4, 8),
    (4, 4, 7),
])
def test_count_seeable(x, y, exp):
    space_map = """
.#..#
.....
#####
....#
...##
"""
    compute = SpaceMap(space_map)
    res = compute.count_seeable(x, y)
    print(f"Test ({x}, {y}) gives {res}")
    assert res == exp


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("""
.#..#
.....
#####
....#
...##""", 8),
    ("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""", 33),
    ("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""", 35),
    ("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""", 41),
    ("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", 210),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def test_angle_order():
    space_map = SpaceMap("""
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##""")
    monitor = (8, 3)
    vaporize = list(space_map.vaporize_order(monitor))
    assert vaporize[0] == (8, 1)
    assert vaporize == [
        (8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1),
        (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4),
        (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2), (1, 0), (5, 1),
        (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1), (13, 3), (14, 3),
    ]


@pytest.mark.parametrize("inp, exp", [
    ("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", 802),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


class SpaceMap:
    def __init__(self, inp_map):
        self._map = [list(row) for row in inp_map.strip().split('\n')]

    def __getitem__(self, pos):
        x, y = pos
        return self._map[y][x]

    def __str__(self):
        return '\n'.join(''.join(row) for row in self._map)

    @property
    def asteroids(self):
        """Yields the position ``(x, y)`` of each asteroids."""
        for y, row in enumerate(self._map):
            for x, cell in enumerate(row):
                if cell == '#':
                    yield(x, y)

    def can_see(self, x1, y1, x2, y2, removed=None):
        """Checks if ``(x1, y1)`` can see object at ``(x2, y2)``.

        This is done by getting the smaller integral vector that goes from position 1 to position 2.
        Once smaller integral vector is known, check all position in between for an asteroid."""
        if removed is None:
            removed = []
        v_x, v_y = x2-x1, y2-y1
        denom = gcd(v_x, v_y)
        v_x = v_x // denom
        v_y = v_y // denom
        for i in range(1, denom):
            pos = (x1+v_x*i, y1+v_y*i)
            if pos in removed:
                continue
            if self[pos] == '#':
                return False
        return True

    def count_seeable(self, x, y):
        """Count the number of seeable asteroids from position ``(x, y)``.

        Don't forget to exclude the tested position from the search."""
        return sum(1 if self.can_see(x, y, a_x, a_y) else 0
                   for a_x, a_y in self.asteroids
                   if (a_x, a_y) != (x, y)
        )

    def best_monitor(self):
        """Gives the asteroid from which we can see the most asteroids."""
        seeable = 0
        best_x = best_y = None
        for x, y in self.asteroids:
            count = self.count_seeable(x, y)
            if count > seeable:
                seeable = count
                best_x, best_y = x, y
        return best_x, best_y

    def vaporize_order(self, monitor):
        """To get all asteroids in correct order:
        For each turn of the laser:
            * Get all visible asteroids. They will all et destroyed.
            * Sort them according to the angle with vertical. atan2 does exactly this.
        """
        to_vaporize = {a for a in self.asteroids if a != monitor}
        removed = set()
        while to_vaporize:
            this_turn = {a for a in to_vaporize if self.can_see(monitor[0], monitor[1], a[0], a[1], removed=removed)}
            removed = removed.union(this_turn)
            to_vaporize -= this_turn
            yield from sorted(this_turn, key=lambda p: atan2(p[0]-monitor[0], p[1]-monitor[1]), reverse=True)

def partOne(inp):
    space_map = SpaceMap(inp)
    return space_map.count_seeable(*space_map.best_monitor())


def partTwo(inp):
    space_map = SpaceMap(inp)
    monitor = space_map.best_monitor()
    vaporization = list(space_map.vaporize_order(monitor))
    vap200 = vaporization[199]
    return vap200[0]*100+vap200[1]


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
