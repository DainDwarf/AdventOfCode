#!/usr/bin/python3
from enum import Enum, unique, auto

@unique
class Direction(Enum):
    NORTH = auto(),
    SOUTH = auto(),
    WEST = auto(),
    EAST = auto(),

    def move(self, pos, val):
        if self is Direction.NORTH:
            return (pos[0]  , pos[1]+val)
        elif self is Direction.SOUTH:
            return (pos[0]  , pos[1]-val)
        elif self is Direction.WEST:
            return (pos[0]-val, pos[1]  )
        elif self is Direction.EAST:
            return (pos[0]+val, pos[1]  )

    @property
    def right(self):
        """Returns the move that corresponds to the right of current direction."""
        if self is Direction.NORTH:
            return Direction.EAST
        elif self is Direction.EAST:
            return Direction.SOUTH
        elif self is Direction.SOUTH:
            return Direction.WEST
        elif self is Direction.WEST:
            return Direction.NORTH

    @property
    def left(self):
        """Returns the move that corresponds to the left of current direction."""
        if self is Direction.NORTH:
            return Direction.WEST
        elif self is Direction.WEST:
            return Direction.SOUTH
        elif self is Direction.SOUTH:
            return Direction.EAST
        elif self is Direction.EAST:
            return Direction.NORTH


class Ship:
    def __init__(self):
        self._pos = (0, 0)
        self._dir = Direction.EAST

    @property
    def pos(self):
        return self._pos

    def move(self, direction, value):
        if direction == 'L':
            for _ in range(value//90):
                self._dir = self._dir.left
        elif direction == 'R':
            for _ in range(value//90):
                self._dir = self._dir.right
        elif direction == 'F':
            self._pos = self._dir.move(self._pos, value)
        elif direction == 'N':
            self._pos = Direction.NORTH.move(self._pos, value)
        elif direction == 'E':
            self._pos = Direction.EAST.move(self._pos, value)
        elif direction == 'W':
            self._pos = Direction.WEST.move(self._pos, value)
        elif direction == 'S':
            self._pos = Direction.SOUTH.move(self._pos, value)
        else:
            raise RuntimeError(f"Unknown direction {direction}")

    def navigate(self, inp):
        for line in inp.split('\n'):
            direction = line[:1]
            value = int(line[1:])
            self.move(direction, value)


class WaypointShip(Ship):
    def __init__(self):
        super().__init__()
        self._way = (10, 1)

    def move(self, direction, value):
        if direction == 'L':
            for _ in range(value//90):
                self._way = (-self._way[1], self._way[0])
        elif direction == 'R':
            for _ in range(value//90):
                self._way = (self._way[1], -self._way[0])
        elif direction == 'F':
            self._pos = (self._pos[0]+value*self._way[0], self._pos[1]+value*self._way[1])
        elif direction == 'N':
            self._way = Direction.NORTH.move(self._way, value)
        elif direction == 'E':
            self._way = Direction.EAST.move(self._way, value)
        elif direction == 'W':
            self._way = Direction.WEST.move(self._way, value)
        elif direction == 'S':
            self._way = Direction.SOUTH.move(self._way, value)
        else:
            raise RuntimeError(f"Unknown direction {direction}")


def part_one(inp):
    ship = Ship()
    ship.navigate(inp)
    return abs(ship.pos[0])+abs(ship.pos[1])


def part_two(inp):
    ship = WaypointShip()
    ship.navigate(inp)
    return abs(ship.pos[0])+abs(ship.pos[1])


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
