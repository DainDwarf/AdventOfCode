

class ThreeStateGameOfLife(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for _ in range(height):
            self.grid.append(['.']*width)

    @classmethod
    def fromDescription(cls, desc):
        desc = desc.strip().split()
        height = len(desc)
        width = max(len(l) for l in desc)
        self = cls(width, height)
        for x, line in enumerate(desc):
            for y, char in enumerate(line):
                self.grid[x][y] = char
        return self

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.grid)

    def __getitem__(self, pos):
        try:
            line, col = pos
            if line >= 0 and col >= 0:
                return self.grid[pos[0]][pos[1]]
            else:
                return None
        except IndexError:
            return None

    def getNeighbors(self, pos):
        line, col = pos
        ret = [ self[(line-1, col-1)],
                self[(line-1, col  )],
                self[(line-1, col+1)],
                self[(line  , col-1)],
                self[(line  , col+1)],
                self[(line+1, col-1)],
                self[(line+1, col  )],
                self[(line+1, col+1)],
        ]
        return [i for i in ret if i is not None]

    def step(self):
        """Do a step given the specifications.

        An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
        An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
        An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open."""
        new_grid = []
        for x, line in enumerate(self.grid):
            new_line = []
            for y, state in enumerate(line):
                neighbors = self.getNeighbors((x, y))
                if state == ".":
                    if neighbors.count("|") >= 3:
                        new_line.append("|")
                    else:
                        new_line.append(".")
                elif state == "|":
                    if neighbors.count("#") >= 3:
                        new_line.append("#")
                    else:
                        new_line.append("|")
                elif state == "#":
                    if neighbors.count("#") >= 1 and neighbors.count("|"):
                        new_line.append("#")
                    else:
                        new_line.append(".")
            new_grid.append(new_line)
        self.grid = new_grid

    def steps(self, count):
        """Detect a loop in state to fast forward steps count."""
        seen_states = {0: self.grid}
        for n in range(1, count+1):
            self.step()
            for prev_n, state in seen_states.items():
                if state == self.grid:
                    print(f"State {n} has already been seen as state {prev_n}.")
                    loop_length = n-prev_n
                    remaining_steps = count-n
                    return self.steps(remaining_steps%loop_length)
            seen_states[n] = self.grid

    def count(self, value):
        return sum(sum(1 if char == value else 0 for char in line) for line in self.grid)

    def resourceValue(self):
        return self.count("|")*self.count("#")


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
    grid = ThreeStateGameOfLife.fromDescription(inp)
    print("Initial state:")
    print(grid)
    print()
    for i in range(10):
        print(f"After {i+1} minutes:")
        grid.step()
        print(grid)
        print()

    res = partOne(inp)
    print(f"The total resource value after ten minutes is {res}.")


def testTwo():
    print("Unit test for Part Two.")

    inp = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
    res = partTwo(inp)
    print(f"The total resource value after a billion minutes is {res}.")


def partOne(inp):
    grid = ThreeStateGameOfLife.fromDescription(inp)
    grid.steps(10)
    return grid.resourceValue()


def partTwo(inp):
    grid = ThreeStateGameOfLife.fromDescription(inp)
    grid.steps(1000000000)
    return grid.resourceValue()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
