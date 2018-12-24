class Cave(object):
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        #Cache of already computed erosion levels.
        self.erosions = dict()

    def __getitem__(self, pos):
        if pos in self.erosions:
            return self.erosions[pos]
        else:
            x, y = pos
            if x < 0 or y < 0:
                raise IndexError
            elif pos == (0, 0) or pos == self.target:
                geol = 0
            elif x == 0:
                geol = y*48271
            elif y == 0:
                geol = x*16807
            else:
                geol = self[(x-1, y)] * self[(x, y-1)]

            ret = (geol + self.depth) % 20183
            self.erosions[pos] = ret
            return ret

    def display(self, endpoint):
        """Displays from 0,0 to given endpoint."""
        endx, endy = endpoint
        for y in range(0, endy+1):
            for x in range(0, endx+1):
                tileType = self[(x, y)] % 3
                if (x, y) == (0, 0):
                    print('M', end='')
                elif (x, y) == self.target:
                    print('T', end='')
                elif tileType == 0:
                    print('.', end='')
                elif tileType == 1:
                    print('=', end='')
                elif tileType == 2:
                    print('|', end='')
            print()

    def riskLevel(self):
        """Computes the risk level from 0,0 to target."""
        endx, endy = self.target
        return sum(sum(self[(x, y)]%3 for x in range(0, endx+1)) for y in range(0, endy+1))


class DijkstraSavior(object):
    """Use Dijkstra's algorithm to save that poor reindeer.

    We consider the nodes as (x, y, tool).
    This means we need to get from (0, 0, "torch") to (targetX, targetY, "torch").

    We adapt the neighbors to return up/down/left/right if they don't require a tool change,
    as well as staying on the same position but switching tool.

    Tools are "torch", "climb", and "neither"."""
    def __init__(self, cave):
        self.cave = cave
        self.visited = {(0, 0, "torch"): 0} #Dictionary of nodes: smallest distance
        self.tentative = self.neighbors((0, 0, "torch"))

    def canUse(self, tool, pos):
        tileType = self.cave[pos]%3
        if tileType == 0: # Rocky
            return tool in ("torch", "climb")
        elif tileType == 1: # Wet
            return tool in ("neither", "climb")
        elif tileType == 2: # Narrow
            return tool in ("neither", "torch")

    def neighbors(self, node):
        """Returns a dict all possible unvisited neighbors, and their relative distance."""
        x, y, tool = node
        n = dict()
        for t in ("torch", "climb", "neither"):
            if t != tool and self.canUse(t, (x, y)):
                n[(x, y, t)] = 7
        if self.canUse(tool, (x+1, y)):
            n[(x+1, y, tool)] = 1
        if self.canUse(tool, (x, y+1)):
            n[(x, y+1, tool)] = 1
        if x > 0 and self.canUse(tool, (x-1, y)):
            n[(x-1, y, tool)] = 1
        if y > 0 and self.canUse(tool, (x, y-1)):
            n[(x, y-1, tool)] = 1
        return n

    def saveTime(self):
        """Compute the minimal distance to save the reindeer."""
        targetX, targetY = self.cave.target
        target = (targetX, targetY, "torch")
        while target not in self.visited and self.tentative:
            current_node, current_distance = min(self.tentative.items(), key=lambda t:t[1])
            for neigh_node, neigh_distance in self.neighbors(current_node).items():
                if neigh_node not in self.visited:
                    if neigh_node in self.tentative:
                        self.tentative[neigh_node] = min(neigh_distance+current_distance, self.tentative[neigh_node])
                    else:
                        self.tentative[neigh_node] = neigh_distance+current_distance
            self.visited[current_node] = current_distance
            self.tentative.pop(current_node)
        return self.visited[target]


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    depth=510
    target = (10, 10)
    c = Cave(depth, target)
    c.display((15, 15))
    res = partOne(depth, target)
    print(f"Risk level of cave depth {depth} to target {target} is {res}.")


def testTwo():
    print("Unit test for Part Two.")

    depth=510
    target = (10, 10)
    c = Cave(depth, target)
    savior = DijkstraSavior(c)
    print(f"Starting possible moves are {savior.tentative}")

    res = partTwo(depth, target)
    print(f"It takes {res} minutes to save the reindeer at {target} on depth {depth}.")


def partOne(depth, target):
    c = Cave(depth, target)
    return c.riskLevel()


def partTwo(depth, target):
    c = Cave(depth, target)
    savior = DijkstraSavior(c)
    return savior.saveTime()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-D", "--depth", help='Your input depth', type=int)
    args.add_argument("-T", "--target", help='Your input target', type=lambda s:tuple(map(int, s.split(','))))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.depth and options.target:
        print("Answer for part one is : {res}".format(res=partOne(options.depth, options.target)))
        print("Answer for part two is : {res}".format(res=partTwo(options.depth, options.target)))
