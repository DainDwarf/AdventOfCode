import re, time


def getUp(pos):
    return (pos[0], pos[1]-1)

def getDown(pos):
    return (pos[0], pos[1]+1)

def getLeft(pos):
    return (pos[0]-1, pos[1])

def getRight(pos):
    return (pos[0]+1, pos[1])


class Water(object):
    """Everything to help doing a deep first search for water flowing."""
    def __init__(self, position, parent=None):
        self.pos = position
        self.parent = parent
        self.state = "flow"


class Ground(object):
    def __init__(self):
        self.clay = set()
        self.spring = (500, 0)
        self.water = dict() #Position: Water. Yes, that's redundant.
        self.minx = 500
        self.maxx = 500
        self.miny = 0
        self.maxy = 0

    @classmethod
    def fromDescription(cls, desc):
        num_re = r"(-?\d+)"
        self = cls()
        for line in desc.split("\n"):
            if line.startswith("x"):
                x, ymin, ymax = list(map(int, re.findall(num_re, line)))
                self.addVerticalClay(x, ymin, ymax)
            elif line.startswith("y"):
                y, xmin, xmax = list(map(int, re.findall(num_re, line)))
                self.addHorizontalClay(y, xmin, xmax)
            else:
                raise RuntimeError(f"Unable to parse line {line}")
        return self

    def addVerticalClay(self, x, ymin, ymax):
        for y in range(ymin, ymax+1):
            self.clay.add((x, y))
        self.miny = min(self.miny, ymin)
        self.maxy = max(self.maxy, ymax)
        self.minx = min(self.minx, x)
        self.maxx = max(self.maxx, x)

    def addHorizontalClay(self, y, xmin, xmax):
        for x in range(xmin, xmax+1):
            self.clay.add((x, y))
        self.miny = min(self.miny, y)
        self.maxy = max(self.maxy, y)
        self.minx = min(self.minx, xmin)
        self.maxx = max(self.maxx, xmax)

    def __getitem__(self, pos):
        x, y = pos
        if (x, y) in self.clay:
            return '#'
        elif (x, y) == self.spring:
            return '+'
        elif (x, y) in self.water:
            return '~' if self.water[(x, y)].state == "full" else "|"
        else:
            return '.'

    def display(self):
        for y in range(self.miny, self.maxy+1):
            print("".join(self[(x, y)] for x in range(self.minx, self.maxx+1)))

    def countWater(self):
        minGiveny = min(t[1] for t in self.clay)
        return sum(1 if t[1] >= minGiveny else 0 for t in self.water.keys())

    def countStillWater(self):
        minGiveny = min(t[1] for t in self.clay)
        return sum(1 if t[1] >= minGiveny and w.state == "full" else 0 for t, w in self.water.items())

    def computeFlow(self, debug=False):
        current_flow = Water(self.spring)
        self.water[self.spring] = current_flow
        while current_flow is not None:
            if debug:
                self.display()
                print()
                time.sleep(0.03)
            up = getUp(current_flow.pos)
            down = getDown(current_flow.pos)
            right = getRight(current_flow.pos)
            left = getLeft(current_flow.pos)

            #Search down first
            if self[down] == '.':
                if down[1] > self.maxy: #Backtrack
                    current_flow.state = "infinity"
                    current_flow = current_flow.parent
                else:
                    current_flow = Water(down, parent=current_flow)
                    self.water[down] = current_flow
            elif down in self.water and self.water[down].state == "infinity":
                #Propagate backtrack
                current_flow.state = "infinity"
                current_flow = current_flow.parent
            #Now, try right/left
            else:
                if self[right] == ".":
                    current_flow = Water(right, parent=current_flow)
                    self.water[right] = current_flow
                elif self[left] == ".":
                    current_flow = Water(left, parent=current_flow)
                    self.water[left] = current_flow
                else: #down, left and right are occupied...
                    #But, we need to check if it is an infinity backtracking or filling backtracking,
                    #and to now in what direction to go?
                    if current_flow.parent is not None and current_flow.parent.pos == left:
                        #Flowing horizontally, left to right
                        if right in self.water:
                            #Propagate backtrack
                            current_flow.state = self.water[right].state
                            current_flow = current_flow.parent
                        else: #Blocked, fill the water
                            current_flow.state = "full"
                            current_flow = current_flow.parent
                    elif current_flow.parent is not None and current_flow.parent.pos == right:
                        #Flowing horizontally, right to left
                        if left in self.water:
                            #Propagate backtrack
                            current_flow.state = self.water[left].state
                            current_flow = current_flow.parent
                        else: #Blocked, fill the water
                            current_flow.state = "full"
                            current_flow = current_flow.parent
                    elif current_flow.parent is not None and current_flow.parent.pos == up:
                        #Left and right occupied, and parent is upward...
                        if left in self.water and right in self.water:
                            #Merging two flow
                            if self.water[left].state == "infinity" or self.water[right].state == "infinity":
                                current_flow.state = "infinity"
                                current_flow = current_flow.parent
                                if self.water[left].state == "full":
                                    #Need to render it as infinity instead! For everythin on the left
                                    retrace_left = left
                                    while retrace_left in self.water:
                                        self.water[retrace_left].state = "infinity"
                                        retrace_left = getLeft(retrace_left)
                                elif self.water[right].state == "full":
                                    #Need to render it as infinity instead! For everythin on the right
                                    retrace_right = right
                                    while retrace_right in self.water:
                                        self.water[retrace_right].state = "infinity"
                                        retrace_right = getRight(retrace_right)
                            else:
                                current_flow.state = "full"
                                current_flow = current_flow.parent
                        elif left in self.water:
                            current_flow.state = self.water[left].state
                            current_flow = current_flow.parent
                        elif right in self.water:
                            current_flow.state = self.water[right].state
                            current_flow = current_flow.parent
                        else:
                            current_flow.state = "full"
                            current_flow = current_flow.parent
        minxWater = min(t[0] for t in self.water.keys())
        maxxWater = max(t[0] for t in self.water.keys())
        self.minx = min(self.minx, minxWater)
        self.maxx = max(self.maxx, maxxWater)


# That's handy, the Advent of Code gives unittests.
def testOne(debug=False):
    print("Unit test for Part One.")

    inp = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    res = partOne(inp, debug)
    print(f"The total number of tiles the water can reach is {res}.")


    #   ......+......
    #   #...........#
    #   #..#.....#..#
    #   #..#.#.#.#..#
    #   #..#.#.#.#..#
    #   #..#.###.#..#
    #   #..#.....#..#
    #   #..#######..#
    #   #...........#
    inp = """x = 497, y=2..7
x=503, y=2..7
y=7, x=498..502
x=499, y=3..4
x=501, y=3..4
y=5, x=499..501
x=494, y=1..8
x=506, y=1..8"""
    res = partOne(inp, debug)
    print(f"The total number of tiles the water can reach is {res}.")

    #   ......+......
    #   .............
    #   #....###....#
    #   #...........#
    #   #.#.........#
    #   #.#.......#.#
    #   #.#.......#.#
    #   #.#########.#
    #   #...........#
    inp = """y = 2, x=499..501
x=496, y=4..7
x=504, y=5..7
y=7, x=497..503
x=494, y=2..8
x=506, y=2..8"""
    res = partOne(inp, debug)
    print(f"The total number of tiles the water can reach is {res}.")


def testTwo(debug=False):
    print("Unit test for Part Two.")

    inp = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    res = partTwo(inp, debug)
    print(f"The total number of tiles that are retained is {res}.")


def partOne(inp, debug=False):
    gr = Ground.fromDescription(inp)
    gr.computeFlow(debug=debug)
    return gr.countWater()


def partTwo(inp, debug=False):
    gr = Ground.fromDescription(inp)
    gr.computeFlow(debug=debug)
    return gr.countStillWater()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    args.add_argument("-d", "--debug", help='Adding some debug output', action="store_true")
    options = args.parse_args()

    if options.test:
        testOne(options.debug)
        print()
        testTwo(options.debug)
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp, options.debug)))
        print("Answer for part two is : {res}".format(res=partTwo(inp, options.debug)))
