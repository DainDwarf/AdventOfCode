import pytest
import re
from itertools import count, product


# That's handy, the Advent of Code gives unittests.
def test_parse():
    inp = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moons = [Moon.from_input(line) for line in inp.strip().split('\n')]
    assert [m.position for m in moons] == [
        (-1, 0, 2),
        (2, -10, -7),
        (4, -8, 8),
        (3, 5, -1),
    ]
    assert all(m.velocity == (0, 0, 0) for m in moons)


# OK, that's ugly
@pytest.mark.parametrize("steps, exp", [
    (1, (
        ( 2,-1, 1), ( 3,-1,-1),
        ( 3,-7,-4), ( 1, 3, 3),
        ( 1,-7, 5), (-3, 1,-3),
        ( 2, 2, 0), (-1,-3, 1),
    )),
    (2, (
        ( 5,-3,-1), ( 3,-2,-2),
        ( 1,-2, 2), (-2, 5, 6),
        ( 1,-4,-1), ( 0, 3,-6),
        ( 1,-4, 2), (-1,-6, 2),
    )),
    (3, (
        ( 5,-6,-1), ( 0,-3, 0),
        ( 0, 0, 6), (-1, 2, 4),
        ( 2, 1,-5), ( 1, 5,-4),
        ( 1,-8, 2), ( 0,-4, 0),
    )),
    (4, (
        ( 2,-8, 0), (-3,-2, 1),
        ( 2, 1, 7), ( 2, 1, 1),
        ( 2, 3,-6), ( 0, 2,-1),
        ( 2,-9, 1), ( 1,-1,-1),
    )),
    (5, (
        (-1,-9, 2), (-3,-1, 2),
        ( 4, 1, 5), ( 2, 0,-2),
        ( 2, 2,-4), ( 0,-1, 2),
        ( 3,-7,-1), ( 1, 2,-2),
    )),
    (6, (
        (-1,-7, 3), ( 0, 2, 1),
        ( 3, 0, 0), (-1,-1,-5),
        ( 3,-2, 1), ( 1,-4, 5),
        ( 3,-4,-2), ( 0, 3,-1),
    )),
    (7, (
        ( 2,-2, 1), ( 3, 5,-2),
        ( 1,-4,-4), (-2,-4,-4),
        ( 3,-7, 5), ( 0,-5, 4),
        ( 2, 0, 0), (-1, 4, 2),
    )),
    (8, (
        ( 5, 2,-2), ( 3, 4,-3),
        ( 2,-7,-5), ( 1,-3,-1),
        ( 0,-9, 6), (-3,-2, 1),
        ( 1, 1, 3), (-1, 1, 3),
    )),
    (9, (
        ( 5, 3,-4), ( 0, 1,-2),
        ( 2,-9,-3), ( 0,-2, 2),
        ( 0,-8, 4), ( 0, 1,-2),
        ( 1, 1, 5), ( 0, 0, 2),
    )),
    (10, (
        ( 2, 1,-3), (-3,-2, 1),
        ( 1,-8, 0), (-1, 1, 3),
        ( 3,-6, 1), ( 3, 2,-3),
        ( 2, 0, 4), ( 1,-1,-1),
    )),
])
def test_steps(steps, exp):
    inp = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moons = [Moon.from_input(line) for line in inp.strip().split('\n')]
    for _ in range(steps):
        move_moons(moons)
    for moon, exp_position in zip(moons, exp[::2]):
        assert moon.position == exp_position
    for moon, exp_velocity in zip(moons, exp[1::2]):
        assert moon.velocity == exp_velocity


@pytest.mark.parametrize("inp, steps, exp", [
    ("""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""", 10, 179),
    ("""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""", 100, 1940),
])
def testOne(inp, steps, exp):
    res = partOne(inp, steps=steps)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""", 2772),
    ("""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""", 4686774924),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


class Moon:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
        self._v_x = 0
        self._v_y = 0
        self._v_z = 0

    regexp = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
    @classmethod
    def from_input(cls, inp):
        """Create the moon based on the input format."""
        x, y, z = cls.regexp.match(inp.strip()).groups()
        return cls(int(x), int(y), int(z))

    @property
    def position(self):
        return (self._x, self._y, self._z)

    @property
    def velocity(self):
        return (self._v_x, self._v_y, self._v_z)

    @property
    def energy(self):
        return (abs(self._x) + abs(self._y) + abs(self._z)) \
            *  (abs(self._v_x) + abs(self._v_y) + abs(self._v_z))

    def apply_gravity(self, other):
        """Apply gravity on this moon based on another moon's position."""
        self._v_x += sign(other._x-self._x)
        self._v_y += sign(other._y-self._y)
        self._v_z += sign(other._z-self._z)

    def apply_velocity(self):
        """Apply velocity. This needs to be done after *all* apply_gravity has been done."""
        self._x += self._v_x
        self._y += self._v_y
        self._z += self._v_z


def move_moons(moons):
    for m1, m2 in product(moons, repeat=2):
        m1.apply_gravity(m2)
    for m in moons:
        m.apply_velocity()


def get_state(moons):
    return tuple(m.position + m.velocity for m in moons)


def partOne(inp, steps=1000):
    moons = [Moon.from_input(line) for line in inp.strip().split('\n')]
    for _ in range(steps):
        move_moons(moons)
    return sum(m.energy for m in moons)


def partTwo(inp):
    moons = [Moon.from_input(line) for line in inp.strip().split('\n')]
    state = get_state(moons)
    known_states= set()
    for step in count(start=1):
        known_states.add(state)
        move_moons(moons)
        state = get_state(moons)
        if state in known_states:
            return step


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
